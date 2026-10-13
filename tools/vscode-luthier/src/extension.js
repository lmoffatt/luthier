const vscode = require('vscode');
const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');

function repository(document) {
  const folder = vscode.workspace.getWorkspaceFolder(document.uri);
  if (!folder || folder.uri.scheme !== 'file') return;
  let root = folder.uri.fsPath;
  for (;;) {
    if (fs.existsSync(path.join(root, 'src/luthier/lib/grammar.lth')) &&
        fs.existsSync(path.join(root, 'src/luthier/cli.py'))) return root;
    const parent = path.dirname(root);
    if (parent === root) return;
    root = parent;
  }
}

function activate(context) {
  const diagnostics = vscode.languages.createDiagnosticCollection('luthier');
  const pending = new Map();
  context.subscriptions.push(diagnostics);
  function parse(document) {
    if (document.uri.scheme !== 'file' || !/\.(lth|lut)$/i.test(document.fileName)) return;
    const root = repository(document);
    if (!root) return;
    const key = document.uri.toString();
    const token = {};
    pending.set(key, token);
    const python = vscode.workspace.getConfiguration('luthier', document.uri).get('pythonPath', 'python3');
    execFile(python, ['-m', 'luthier.cli', 'parse', document.fileName], {
      cwd: root, env: { ...process.env, PYTHONPATH: path.join(root, 'src') }
    }, (error, stdout, stderr) => {
      if (pending.get(key) !== token || document.isClosed) return;
      pending.delete(key);
      if (!error) { diagnostics.delete(document.uri); return; }
      const results = [];
      for (const line of (stdout + '\n' + stderr).split(/\r?\n/)) {
        const match = /^(.*):(\d+):(\d+): (.*)$/.exec(line);
        if (!match) continue;
        const position = document.validatePosition(new vscode.Position(
          Math.max(0, Number(match[2]) - 1), Math.max(0, Number(match[3]) - 1)));
        const diagnostic = new vscode.Diagnostic(new vscode.Range(position, position), match[4], vscode.DiagnosticSeverity.Error);
        diagnostic.source = 'luthier parse';
        results.push(diagnostic);
      }
      if (!results.length) {
        const diagnostic = new vscode.Diagnostic(new vscode.Range(0, 0, 0, 0),
          `Could not run luthier parse: ${stderr.trim() || error.message}`, vscode.DiagnosticSeverity.Error);
        diagnostic.source = 'luthier parse';
        results.push(diagnostic);
      }
      diagnostics.set(document.uri, results);
    });
  }
  context.subscriptions.push(
    vscode.workspace.onDidOpenTextDocument(parse),
    vscode.workspace.onDidSaveTextDocument(parse),
    vscode.workspace.onDidCloseTextDocument(document => {
      pending.delete(document.uri.toString());
      diagnostics.delete(document.uri);
    }),
    { dispose() { pending.clear(); } }
  );
  vscode.workspace.textDocuments.forEach(parse);
}
module.exports = { activate };

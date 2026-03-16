async function main() {
  let pyodide = await loadPyodide();
  let output = document.getElementById("output");
  let result = await pyodide.runPythonAsync(`
    from pyodide.http import pyfetch
    response = await pyfetch("app.py")
    with open("app.py", "wb") as f:
      f.write(await response.bytes())
    exec(open("app.py").read())
  `);
  output.innerText = result;
}
main();  // Auto-run on load

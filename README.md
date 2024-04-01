# Bootstrap Theme Compiler

This is a simple script that compiles a Bootstrap theme from a SCSS file. It uses the `sass` command line tool to compile the SCSS file into a CSS file.

## Usage

You need to have Node and Python installed on your system.

To clone this repo and install the dependencies, run the following command:

```bash
git clone https://github.com/sirius-beck/bootstrap-theme-compiler.git
cd bootstrap-theme-compiler
npm install
```

Or use the inline command:

```bash
git clone https://github.com/sirius-beck/bootstrap-theme-compiler.git && cd bootstrap-theme-compiler && npm install
```

To create a new theme, create a new SCSS file in the `src` directory, all the bootstrap variables should be defined in this file (see `src/sample.scss` for an example). Then run the following command:

```bash
npm run start
```

This will compile the SCSS file into a CSS file and save it in the `dist` directory. To change the output folder, change the `output` variable in the `scripts/compile.py` file (line `25`).

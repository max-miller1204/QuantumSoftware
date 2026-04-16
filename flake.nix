{
  description = "QuantumSoftware course environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python313;

        tex = pkgs.texlive.combine {
          inherit (pkgs.texlive) scheme-medium;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            tex
            pkgs.pandoc
          ];

          shellHook = ''
            VENV_DIR="$PWD/.venv"
            if [ ! -f "$VENV_DIR/.setup-done" ]; then
              rm -rf "$VENV_DIR"
              echo "Creating venv..."
              ${python}/bin/python -m venv "$VENV_DIR"
              "$VENV_DIR/bin/pip" install --quiet \
                numpy scipy matplotlib networkx \
                jupyter notebook nbconvert ipykernel \
                qiskit cookiecutter
              if [ -d "$PWD/montecarlo-pkg" ]; then
                "$VENV_DIR/bin/pip" install --quiet -e "$PWD/montecarlo-pkg"
              fi
              "$VENV_DIR/bin/python" -m ipykernel install --user --name quantumsoftware --display-name "QuantumSoftware"
              touch "$VENV_DIR/.setup-done"
            fi
            export PATH="$VENV_DIR/bin:$PATH"

            # Make nix-provided tools (pandoc, xelatex) visible inside the venv
            export PATH="${tex}/bin:${pkgs.pandoc}/bin:$PATH"

            # Keep tool configs scoped to the project
            export COOKIECUTTER_CONFIG="$PWD/.config/cookiecutter"
            export MPLCONFIGDIR="$PWD/.config/matplotlib"
            export JUPYTER_CONFIG_DIR="$PWD/.config/jupyter"
            export JUPYTER_DATA_DIR="$PWD/.local/share/jupyter"

            echo "QuantumSoftware dev shell ready."
          '';
        };
      }
    );
}

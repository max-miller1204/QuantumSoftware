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
          inherit (pkgs.texlive) scheme-full;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            tex
            pkgs.pandoc
            pkgs.git
          ];

          shellHook = ''
            VENV_DIR="$PWD/.venv"
            if [ ! -d "$VENV_DIR" ]; then
              echo "Creating venv..."
              ${python}/bin/python -m venv "$VENV_DIR"
              "$VENV_DIR/bin/pip" install --quiet \
                numpy scipy matplotlib networkx \
                jupyter notebook nbconvert ipykernel \
                qiskit cookiecutter
              "$VENV_DIR/bin/pip" install --quiet -e "$PWD/montecarlo-pkg"
              "$VENV_DIR/bin/python" -m ipykernel install --user --name quantumsoftware --display-name "QuantumSoftware"
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

{
  description = "flask";
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

  outputs = {nixpkgs, self, ...}: let
    forEachSystem = f: nixpkgs.lib.genAttrs ["aarch64-linux" "x86_64-linux"] (system: f (import nixpkgs {inherit system;}));
  in {
    devShells = forEachSystem (pkgs: {
      default = pkgs.mkShell {
        buildInputs = [
          (pkgs.python3.withPackages (pypkgs: with pypkgs; [
            flask
          ]))
        ];
      };
    });

    # TODO: package our repo as a python package and add to docker image
    packages = forEachSystem (pkgs: rec {
      default = pkgs.writeShellApplication {
        name = "dis-flask-project";
        runtimeInputs = with pkgs; [
          (python3.withPackages (p: [p.flask]))
          sqlite
        ];
        text = ''
          cd ${./.}
          flask run
        '';
      };
      docker-image = pkgs.dockerTools.buildLayeredImage {
        name = "ku-dis-flask-project";
        tag = "latest";
        contents = [
          default
        ];
      };
    });

  };
}
{
  description = "flask";
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

  outputs =
    { nixpkgs, self, ... }:
    let
      forEachSystem =
        f:
        nixpkgs.lib.genAttrs [ "aarch64-linux" "x86_64-linux" ] (
          system: f (import nixpkgs { inherit system; })
        );
    in
    {
      devShells = forEachSystem (pkgs: {
        default = pkgs.mkShell {
          buildInputs = [
            (pkgs.python3.withPackages (
              pypkgs: with pypkgs; [
                flask
              ]
            ))
          ];
        };
      });

      apps = forEachSystem (pkgs: {
        default = {
          type = "app";
          program =
            ""
            + (pkgs.writeShellScript "copy-docker-image-from-store" ''
              cp ${self.packages.${pkgs.stdenv.system}.docker-image} ./docker-image.tar.gz
              chmod 755 ./docker-image.tar.gz
            '');
        };
      });

      # TODO: package our repo as a python package and add to docker image
      packages = forEachSystem (pkgs: rec {
        flask-app = pkgs.writeShellApplication {
          name = "dis-flask-project";
          runtimeInputs = with pkgs; [
            (python3.withPackages (p: [ p.flask ]))
            sqlite
          ];
          text =
            let
              src = builtins.path {
                path = ./.;
                filter = (
                  path: type:
                  !(builtins.elem (builtins.baseNameOf path) [
                    "docker-image.tar.gz"
                    ".vscode"
                    ".editorconfig"
                    "flake.nix"
                    "flake.lock"
                    "ReadMe.md"
                  ])
                );
              };
            in
            ''
              DIS_DATABASE=$(pwd)/app.db
              export DIS_DATABASE
              cd ${src}
              flask run $@
            '';
          excludeShellChecks = [ "SC2068" ];
        };
        docker-image = pkgs.dockerTools.buildLayeredImage {
          name = "ku-dis-flask-project";
          tag = "latest";
          contents = [
            flask-app
          ];
        };
      });

    };
}

{
  description = "A GNOME extension to make updating your Nix system a bit more convenient.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      packages = forAllSystems (
        system:
        let
          pkgs = (import nixpkgs { inherit system; });
          gnome-shell-extension-molasses-update-nix = pkgs.callPackage ./package.nix { };
        in
        {
          inherit gnome-shell-extension-molasses-update-nix;
          default = gnome-shell-extension-molasses-update-nix;
        }
      );

      nixosModules.molasses-update-nix = ./nixos-module.nix;
    };
}

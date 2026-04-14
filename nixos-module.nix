{
  config,
  lib,
  pkgs,
  inputs,
  ...
}:
let
  molasses-update-nix = config.molasses-update-nix;
  cfg = config.services.molasses-update-nix;
in
{
  options = {
    molasses-update-nix = {
      enable = lib.mkOption {
        default = false;
        type = with lib.types; bool;
      };
    };
  };

  config = lib.mkIf molasses-update-nix.enable {
    environment.systemPackages = [
      (pkgs.callPackage ./package.nix)
    ];

    services.molasses-update-nix.enable = true;
  };
}

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
    system.configurationRevision =
      let
        self = inputs.self;
      in
      self.shortRev or self.dirtyShortRev or self.lastModified or "molasses-update-nix";
  };

  services.molasses-update-nix.enable = true;

  config.environment.systemPackages = [
    (pkgs.callPackage ./package.nix)
  ];
}

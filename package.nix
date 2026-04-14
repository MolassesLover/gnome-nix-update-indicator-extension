{ stdenv }:

stdenv.mkDerivation (finalAttrs: {
  name = "gnome-shell-extension-molasses-update-nix";
  version = "1.0.0";
  src = ./src;

  installPhase = ''
    			runHook preInstall
      		install -Dm755 ./py/molasses-update-nix.py $out/bin/molasses-update-nix;
        	mkdir -p $out/share/gnome-shell/extensions/
        	cp -r  ./js/gnome-nix-update@molasses.love $out/share/gnome-shell/extensions
        	runHook postInstall
        	'';

  passthru.extensionUuid = "gnome-nix-update@molasses.love";
})

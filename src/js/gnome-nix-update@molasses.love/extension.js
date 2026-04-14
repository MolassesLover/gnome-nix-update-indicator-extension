import GObject from "gi://GObject";
import Gio from "gi://Gio";
import St from "gi://St";

import {
  Extension,
  gettext as _,
} from "resource:///org/gnome/shell/extensions/extension.js";

import * as PanelMenu from "resource:///org/gnome/shell/ui/panelMenu.js";
import * as PopupMenu from "resource:///org/gnome/shell/ui/popupMenu.js";

import * as Main from "resource:///org/gnome/shell/ui/main.js";

function check_update_callback() {
  console.log("Finished execution.");
  Main.notify(_("Updated NixOS system! C:"));
}
async function update() {
  Main.notify(_("Updating NixOS system."));

  try {
    const proc = Gio.Subprocess.new(
      ["xdg-terminal", "molasses-update-nix"],

      Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
    );

    const cancellable = new Gio.Cancellable();

    const [stdout, stderr] = await proc.communicate_utf8_async(
      null,
      cancellable,
      check_update_callback,
    );

    if (proc.get_successful()) console.log(stdout);
    else throw new Error(stderr);
  } catch (error) {
    logError(error);
  }
}

// Not yet implemented.
async function check_update() {
  Main.notify(_("Checking for updates..."));

  try {
    const proc = Gio.Subprocess.new(
      ["xdg-terminal", "molasses-update-nix --check"],

      Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
    );

    const cancellable = new Gio.Cancellable();

    const [stdout, stderr] = await proc.communicate_utf8_async(
      null,
      cancellable,
      check_update_callback,
    );

    if (proc.get_successful()) console.log(stdout);
    else throw new Error(stderr);
  } catch (error) {
    logError(error);
  }
}

const Indicator = GObject.registerClass(
  class Indicator extends PanelMenu.Button {
    _init() {
      super._init(0.0, _("Nix Update Indicator"));

      this.add_child(
        new St.Icon({
          gicon: new Gio.ThemedIcon({
		name: 'emote-love-symbolic'
	   }),
          style_class: "system-status-icon",
        }),
      );

      let item_update = new PopupMenu.PopupMenuItem(_("Update now"));
      item_update.connect("activate", () => {
        update();
      });
      this.menu.addMenuItem(item_update);

      //let item_check = new PopupMenu.PopupMenuItem(_("Check now"));
      //item_check.connect("activate", () => {
      //  check_update();
      //});
      //this.menu.addMenuItem(item_check);
    }
  },
);

export default class IndicatorExampleExtension extends Extension {
  enable() {
    this._indicator = new Indicator();
    Main.panel.addToStatusArea(this.uuid, this._indicator);
  }

  disable() {
    this._indicator.destroy();
    this._indicator = null;
  }
}

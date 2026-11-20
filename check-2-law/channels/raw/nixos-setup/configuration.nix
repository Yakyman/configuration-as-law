{ config, pkgs, ... }:
{
 imports = [ ./hardware-configuration.nix ];
 boot.loader.grub.enable = true;
 boot.loader.grub.device = "/dev/vda";
 boot.kernelParams = [ "console=ttyS0,115200n8" ];
 networking.hostName = "d2-nixos";
 networking.useDHCP = true;
 services.openssh.enable = true;
 services.openssh.settings.PermitRootLogin = "prohibit-password";
 users.users.root.openssh.authorizedKeys.keys = [ "<REDACTED-11>" ];
 users.users.alice = {
  isNormalUser = true;
  extraGroups = [ ];
  openssh.authorizedKeys.keys = [ "<REDACTED-11>" ];
 };
 environment.systemPackages = with pkgs; [ (python3.withPackages (p: [ p.pip p.setuptools p.wheel ])) nodejs cargo rustc gcc curl wget chromium flatpak appimage-run bubblewrap util-linux patchelf jq git at tmux dbus xdg-utils dex ];
 services.cron.enable = true;
 services.atd.enable = true;
 services.flatpak.enable = true;
 xdg.portal.enable = true;
 xdg.portal.extraPortals = [ pkgs.xdg-desktop-portal-gtk ];
 virtualisation.podman.enable = true;
 nix.settings.max-jobs = 2;
 nix.settings.cores = 2;
 system.stateVersion = "26.05";
}

{ config, pkgs, ... }:
{
  imports = [ ./hardware-configuration.nix ];
  boot.loader.grub.enable = true;
  boot.loader.grub.device = "/dev/vda";
  boot.kernelParams = [ "console=ttyS0,115200n8" ];
  networking.hostName = "v1-nixos";
  networking.useDHCP = true;
  services.openssh.enable = true;
  users.users.census = {
    isNormalUser = true;
    extraGroups = [ "wheel" ];
    openssh.authorizedKeys.keys = [ "<REDACTED-6>" ];
  };
  security.sudo.wheelNeedsPassword = false;
  nix.settings.max-jobs = 2;
  nix.settings.cores = 2;
  system.stateVersion = "26.05";
}

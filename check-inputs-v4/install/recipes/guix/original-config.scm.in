(use-modules (gnu))
(use-service-modules networking base)
(operating-system
  (host-name "cal")
  (timezone "UTC")
  (locale "en_US.utf8")
  (kernel-arguments (append '("console=ttyS0,115200n8") %default-kernel-arguments))
  (bootloader (bootloader-configuration
                (bootloader grub-bootloader)
                (targets '("/dev/vda"))))
  (file-systems (cons (file-system
                       (device (file-system-label "root"))
                       (mount-point "/")
                       (type "ext4"))
                     %base-file-systems))
  (users (cons (user-account
                (name "user")
                (group "users")
                (password "$6$cal1122$ZIs03fvnBPSkasZ1B2RLSUt5dtUPGWVefzUbzC/CFnMSXK4xzJO5MQW1e3hyUIucJpFf/YLlootGG36zQ6EqB0")
                (supplementary-groups '("wheel" "netdev")))
               %base-user-accounts))
  (services (append (list (service dhcp-client-service-type)
                          (service agetty-service-type
                            (agetty-configuration (tty "ttyS0") (baud-rate "115200"))))
                    %base-services)))

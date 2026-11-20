(use-modules (gnu home) (gnu services) (gnu home services) (guix gexp))
(home-environment
 (services
  (list
   (simple-service 'w1-declared-note home-files-service-type
                   (list `( ".config/w1/declared-note"
                            ,(plain-file "w1-declared-note" "This file belongs to the user's Home declaration.\n")))))))

(load-this-project
 `( (:search-extensions (".py"))
    (:extra-search-directories (,*pygments-src-dir*))
    (:python-executable ,*python-3-executable*)
    (:run-project-command (python-run-main-file) ) ) )

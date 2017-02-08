Notes
=====


Notes on maintaining this website which operates by using the static
site generator Jekyll on GitHub Pages.


References
----------

* GitHub pages basics:
  https://help.github.com/categories/github-pages-basics
* GitHub pages advanced:
  https://help.github.com/categories/customizing-github-pages
* Jekyll: https://jekyllrb.com/


Website Update Process
----------------------

* Create a branch for your updates
* Make your edits
* Optionally preview your work with Jekyll locally (https://jekyllrb.com/docs/usage/)
  * Installing Jekyll on Fedora:
    https://developer.fedoraproject.org/start/sw/web-app/jekyll.html

    sudo dnf install ruby-devel
    sudo dnf install libffi-devel # I also needed libffi
    gem install jekyll bundler # https://jekyllrb.com/docs/quickstart/
    bundle exec jekyll serve & # Run in background but not detached

  * Use `gem outdated` to see what gems can be updated and `gem update`
    to update them
* Push your branch
* Merge the branch into `master`


Style
-----

* Use the Python convention of wrapping lines at 72 characters (Emacs
  does this well with variable `fill-column`)
* Headers with `=` and `-` "underline" style
* Two blank lines before a header, one blank line after
* Two spaces between sentences
* Copyright for file formats with comments (code, data) goes at the top
  after a brief description
* Copyright for Markdown and other content goes at the bottom (in the
  footer)
* Use the existing style in the file if unsure

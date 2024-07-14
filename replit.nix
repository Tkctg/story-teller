{ pkgs }: {
  deps = [
    pkgs.python39
    pkgs.python39Packages.pip
    pkgs.python39Packages.flask
  ];

  postBuild = ''
    python3 -m pip install -r requirements.txt
  '';
}

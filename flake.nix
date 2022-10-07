{
  inputs = {
    nixpkgs.url = "github:StarGate01/nixpkgs/bip_utils_update";
  };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in
    {
      devShell.x86_64-linux =
        pkgs.mkShell {
          shellHook = ''
          '';

          buildInputs = with pkgs; [
            (python3.withPackages (ps: with ps; [
              cryptography
              asn1
              pyscard
              bip_utils
            ]))
          ];
        };
    };
}

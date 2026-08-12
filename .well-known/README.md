# Digital Asset Links — read this before touching `assetlinks.json`

`assetlinks.json` is the file Android reads to decide whether the Codex app
is allowed to open `https://<this origin>/…` without a browser address bar.
It is a **placeholder** until two things are settled.

## 1. It does not verify from where the Codex is published today

A Trusted Web Activity checks exactly one URL:

    https://<origin>/.well-known/assetlinks.json

Note the **origin root**. The Codex is currently served from a GitHub Pages
*project* path — `https://bennyzrealty-sys.github.io/codex/` — so this file
deploys to `…/codex/.well-known/assetlinks.json`, which Android never looks
at. The root of that origin belongs to a repository named
`bennyzrealty-sys.github.io`, not to this one.

Two ways out, either of which makes this file live:

1. **A custom domain** (e.g. `codex.homeberry.ai`, on Pages or Vercel). Then
   this repository *is* the origin root and the file is served correctly.
   This is the recommended route — it is also the only one that looks like a
   product rather than a side project.
2. **A `bennyzrealty-sys.github.io` user-pages repository** that serves the
   assetlinks file at its root. The Codex stays where it is; the asset links
   live somewhere else and have to be kept in step by hand.

`.nojekyll` in the repository root is what makes GitHub Pages serve this
directory at all — Jekyll skips paths beginning with a dot.

## 2. The fingerprint does not exist yet

Both placeholder values come from the Android build:

    npx @bubblewrap/cli init --manifest https://<origin>/manifest.json
    npx @bubblewrap/cli build

`bubblewrap` prints the SHA-256 fingerprint of the signing key it generated,
and the `applicationId` it used. Paste them into `package_name` and
`sha256_cert_fingerprints`, deploy, and verify with:

    curl https://<origin>/.well-known/assetlinks.json

If the app still shows a URL bar, the file is being served from the wrong
origin, is not `application/json`, or the fingerprint belongs to a different
keystore than the one that signed the uploaded bundle. Google Play App
Signing re-signs the upload, so once the app is on Play the fingerprint that
must appear here is the one Play shows under **Setup → App integrity**, not
the local keystore's.

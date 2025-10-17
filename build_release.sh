#!/bin/bash
set -e

VERSION="0.1"
APP_NAME="CTMU"
BUILD_DIR="build"
DIST_DIR="dist"
PKG_DIR="$BUILD_DIR/pkg"
DMG_DIR="$BUILD_DIR/dmg"

echo "Building CTMU v$VERSION release packages..."

# Clean previous builds
rm -rf $BUILD_DIR $DIST_DIR
mkdir -p $PKG_DIR $DMG_DIR $DIST_DIR

# Create application bundle structure
APP_BUNDLE="$PKG_DIR/$APP_NAME.app"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Create Info.plist
cat > "$APP_BUNDLE/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ctmu</string>
    <key>CFBundleIdentifier</key>
    <string>org.freew.ctmu</string>
    <key>CFBundleName</key>
    <string>CTMU</string>
    <key>CFBundleVersion</key>
    <string>$VERSION</string>
    <key>CFBundleShortVersionString</key>
    <string>$VERSION</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
EOF

# Create executable wrapper
cat > "$APP_BUNDLE/Contents/MacOS/ctmu" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/../Resources"
python3 -m ctmu.cli "$@"
EOF
chmod +x "$APP_BUNDLE/Contents/MacOS/ctmu"

# Copy source files
cp -r src "$APP_BUNDLE/Contents/Resources/"
cp requirements.txt "$APP_BUNDLE/Contents/Resources/"
cp README.md "$APP_BUNDLE/Contents/Resources/"

# Create PKG installer
echo "Creating PKG installer..."
pkgbuild --root "$PKG_DIR" \
         --identifier "org.freew.ctmu" \
         --version "$VERSION" \
         --install-location "/Applications" \
         "$DIST_DIR/CTMU-$VERSION.pkg"

# Sign PKG with GPG
echo "Signing PKG with GPG..."
if [ -n "$GPG_PASSPHRASE" ]; then
    echo "$GPG_PASSPHRASE" | gpg --batch --yes --pinentry-mode loopback --passphrase-fd 0 --detach-sign --armor --default-key jnc@freew.org "$DIST_DIR/CTMU-$VERSION.pkg"
else
    gpg --detach-sign --armor --default-key jnc@freew.org "$DIST_DIR/CTMU-$VERSION.pkg"
fi

# Create DMG
echo "Creating DMG..."
cp -r "$APP_BUNDLE" "$DMG_DIR/"
cp README.md "$DMG_DIR/"

# Create DMG image
hdiutil create -volname "CTMU $VERSION" \
               -srcfolder "$DMG_DIR" \
               -ov -format UDZO \
               "$DIST_DIR/CTMU-$VERSION.dmg"

# Sign DMG with GPG
echo "Signing DMG with GPG..."
if [ -n "$GPG_PASSPHRASE" ]; then
    echo "$GPG_PASSPHRASE" | gpg --batch --yes --pinentry-mode loopback --passphrase-fd 0 --detach-sign --armor --default-key jnc@freew.org "$DIST_DIR/CTMU-$VERSION.dmg"
else
    gpg --detach-sign --armor --default-key jnc@freew.org "$DIST_DIR/CTMU-$VERSION.dmg"
fi

# Create checksums
echo "Creating checksums..."
cd $DIST_DIR
shasum -a 256 *.pkg *.dmg > CTMU-$VERSION-checksums.txt
if [ -n "$GPG_PASSPHRASE" ]; then
    echo "$GPG_PASSPHRASE" | gpg --batch --yes --pinentry-mode loopback --passphrase-fd 0 --clearsign --default-key jnc@freew.org CTMU-$VERSION-checksums.txt
else
    gpg --clearsign --default-key jnc@freew.org CTMU-$VERSION-checksums.txt
fi

echo "Release packages created:"
ls -la CTMU-$VERSION.*
echo "Build complete!"
EOF
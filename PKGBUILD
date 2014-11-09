# Maintainer: Maximilian Kindshofer <maximilian@kindshofer.net>
pkgname=python-woodhouse
pkgver=1.0.0
pkgrel=1
pkgdesc="Folder decluttering tool like hatzle"
arch=()
url="https://github.com/MaximilianKindshofer/Woodhouse"
license=('GPL')
depends=('python', 'python-pyside')
makedepends=('git')
provides=('woodhouse')
md5sums=('SKIP')

source=('woodhouse::git+https://github.com/MaximilianKindshofer/Woodhouse.git')

build() {
    cd ${srcdir}
}

package() {
    cd "$srcdir/$pkgname"

    install -D -m755 woodhouse /usr/bin/woodhouse
    install -D -m755 woodhouse.py /usr/lib/woodhouse/woodhouse.py

    install -D -m755 woodhouse_function.py
    ${pkdir}/usr/lib/woodhouse/woodhouse_function.py || return 1
    install -D -m644 active.png 
    ${pkgdir}/usr/share/pixmaps/woodhouse/active.png
    install -D -m644 deactive.png 
    ${pkdir}/usr/share/pixmaps/woodhouse/deactive.png
    install -D -m644 woodhouse.png
    ${pkgdir}/usr/share/pixmaps/woodhouse/woodhouse.png
    install -D -m644 rules.conf ${pkgdir}/{$HOME}/.woodhouse/rules.conf
}

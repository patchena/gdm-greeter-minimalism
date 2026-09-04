#!/usr/bin/env bash
set -euo pipefail

version="1.0.4"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(readlink -f "${script_dir}/..")"
release_dir="${project_root}/release/v${version}"
package_root="${release_dir}/package"
debian_dir="${package_root}/DEBIAN"
binary_dir="${package_root}/usr/bin"
autostart_dir="${package_root}/etc/xdg/autostart"
doc_dir="${package_root}/usr/share/doc/gdm-greeter-minimalism"
man_dir="${package_root}/usr/share/man/man1"
package_file="${release_dir}/gdm-greeter-minimalism_${version}_all.deb"

install -d -m755 "${debian_dir}" "${binary_dir}" "${autostart_dir}" "${doc_dir}" "${man_dir}"
install -m644 "${project_root}/packaging/control" "${debian_dir}/control"
install -m644 "${project_root}/packaging/conffiles" "${debian_dir}/conffiles"
install -m644 "${project_root}/packaging/triggers" "${debian_dir}/triggers"
install -m755 "${project_root}/packaging/postinst" "${debian_dir}/postinst"
install -m755 "${project_root}/packaging/prerm" "${debian_dir}/prerm"
install -m755 "${project_root}/scripts/gdm-greeter-minimalism.sh" "${binary_dir}/gdm-greeter-minimalism"
install -m644 "${project_root}/packaging/gdm-greeter-minimalism-notify.desktop" "${autostart_dir}/gdm-greeter-minimalism-notify.desktop"
install -m644 "${project_root}/packaging/copyright" "${doc_dir}/copyright"
install -m644 "${project_root}/README.md" "${doc_dir}/README.md"
install -m644 "${project_root}/docs/description.md" "${doc_dir}/description.md"
gzip -cn9 "${project_root}/packaging/changelog" >"${doc_dir}/changelog.gz"
chmod 644 "${doc_dir}/changelog.gz"
gzip -cn9 "${project_root}/packaging/gdm-greeter-minimalism.1" >"${man_dir}/gdm-greeter-minimalism.1.gz"
chmod 644 "${man_dir}/gdm-greeter-minimalism.1.gz"
chmod 755 \
    "${package_root}" \
    "${package_root}/etc" \
    "${package_root}/etc/xdg" \
    "${package_root}/usr" \
    "${package_root}/usr/share" \
    "${package_root}/usr/share/doc" \
    "${package_root}/usr/share/man"

dpkg-deb --root-owner-group --build "${package_root}" "${package_file}"
printf '%s\n' "${package_file}"

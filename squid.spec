Name: squid
Version: 2.5.STABLE7
Release: alt4

Summary: The Squid proxy caching server
License: GPL
Group: System/Servers

Url:http://www.%name-cache.org/Squid
Packager: Squid Development Team <squid@packages.altlinux.org>

Source: %url/v2/%name-%version.tar.bz2
Source1: %url/FAQ/FAQ.sgml
Source2: %name.init
Source3: %name.logrotate

# Other patches
# rediffed for 2.5.S7
Patch1: %name-2.5.STABLE7-make.patch
# rediffed for 2.5.S7
Patch2: %name-2.5.STABLE7-config.patch
Patch3: %name-2.4.STABLE6-alt-without-bind.patch
Patch4: %name-2.5-perlpath.patch
Patch5: %name-2.5-automake.patch
Patch6: %name-errrors-belarusian.patch
Patch7: patch-aa.patch

#Official patches to Squid
# merged into 2.5.STABLE7
Patch10: squid-2.5.STABLE7-half_closed_POST.patch
Patch11: squid-2.5.STABLE7-LDAP_version_documentation.patch
Patch12: squid-2.5.STABLE7_req_resp_header.patch
Patch13: squid-2.5.STABLE7-helper_shutdown.patch
Patch14: squid-2.5.STABLE7-non_blocking_disk.patch
Patch15: squid-2.5.STABLE7-blank_response.patch
Patch16: squid-2.5.STABLE7-dothost.patch
Patch17: squid-2.5.STABLE7-httpd_accel_vport.patch
Patch18: squid-2.5.STABLE7-cachemgr_vmobjects.patch

Obsoletes: %name-novm

BuildConflicts: bind-devel
BuildPreReq: rpm-build >= 4.0.4-alt10, autoconf >= 2.54

# Automatically added by buildreq on Fri Jul 23 2004 (-bi)
BuildRequires: OpenSP libldap-devel libpam-devel libsasl2-devel libssl-devel perl-Authen-Smb sgml-tools

%description
Squid is a high-performance proxy caching server for Web clients,
supporting FTP, gopher, and HTTP data objects. Unlike traditional
caching software, Squid handles all requests in a single,
non-blocking, I/O-driven process. Squid keeps meta data and especially
hot objects cached in RAM, caches DNS lookups, supports non-blocking
DNS lookups, and implements negative caching of failed requests.

Squid consists of a main server program squid, a Domain Name System
lookup program (dnsserver), a program for retrieving FTP data
(ftpget), and some management and client tools.

Install squid if you need a proxy caching server.

%package pinger
Summary: The pinger process for Squid proxy caching server
Group: System/Servers
Requires: %name = %version-%release

%description pinger
Pinger process for Squid to send and receive
ICMP messages directly

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

%build
%set_autoconf_version 2.5

%__autoconf
%configure \
	--bindir=%_sbindir \
	--libexecdir=%_libdir/%name \
	--localstatedir=%_var \
	--sysconfdir=%_sysconfdir/%name \
	--datadir=%_datadir/%name \
	--enable-poll \
	--enable-snmp \
	--enable-removal-policies="lru heap" \
	--enable-delay-pools \
	--enable-icmp \
	--enable-async-io=16 \
	--enable-useragent-log \
	--enable-wccp \
	--with-gnu-regex \
	--enable-arp-acl \
	--enable-ssl \
	--enable-forw-via-db \
	--enable-carp \
	--enable-ntlm-fail-open \
	--enable-cache-digests \
	--enable-x-accelerator-vary \
	--enable-auth="basic ntlm digest" \
	--enable-basic-auth-helpers="LDAP MSNT NCSA PAM SASL SMB YP getpwnam multi-domain-NTLM winbind" \
	--enable-ntlm-auth-helpers="SMB fakeauth no_check winbind" \
	--enable-digest-auth-helpers="password" \
	--enable-external-acl-helpers="ip_user ldap_group unix_group wbinfo_group winbind_group" \
	--enable-storeio="aufs coss diskd null ufs" \
	--enable-default-err-language="English"

%__subst 's/^#define SQUID_MAXFD 1024/#define SQUID_MAXFD 16384/' include/autoconf.h
%make_build

%__mkdir faq
%__cp $RPM_SOURCE_DIR/FAQ.sgml faq
pushd faq
sgml2html FAQ.sgml
popd

%install
%make_build install DESTDIR=$RPM_BUILD_ROOT
%make_build install-pinger DESTDIR=$RPM_BUILD_ROOT

%__mkdir_p $RPM_BUILD_ROOT%_initdir
%__mkdir_p $RPM_BUILD_ROOT%_sysconfdir/logrotate.d
%__install -m 755 $RPM_SOURCE_DIR/%name.init $RPM_BUILD_ROOT%_initdir/%name
%__install -m 644 $RPM_SOURCE_DIR/%name.logrotate $RPM_BUILD_ROOT%_sysconfdir/logrotate.d/%name

%__mkdir_p $RPM_BUILD_ROOT%_logdir/%name
%__mkdir_p $RPM_BUILD_ROOT%_spooldir/%name

%__rm -f $RPM_BUILD_DIR/%name-%version/doc/Programming-Guide/Makefile

%__install -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/PAM/pam_auth.8 $RPM_BUILD_ROOT%_man8dir
%__install -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/external_acl/ldap_group/squid_ldap_group.8 $RPM_BUILD_ROOT%_man8dir
%__install -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/LDAP/squid_ldap_auth.8 $RPM_BUILD_ROOT%_man8dir
%__install -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/external_acl/unix_group/squid_unix_group.8 $RPM_BUILD_ROOT%_man8dir
%__install -p -m644 $RPM_BUILD_DIR/%name-%version/doc/%name.8 $RPM_BUILD_ROOT%_man8dir

%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/SMB/COPYING-2.0 helpers/doc/SMB.COPYING-2.0
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/SMB/README helpers/doc/SMB.README
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/SMB/smb_auth.sh helpers/doc/smb_auth.sh
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/SMB/ChangeLog helpers/doc/SMB.ChangeLog
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/LDAP/README helpers/doc/LDAP.README
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/MSNT/COPYING-2.0 helpers/doc/MSNT.COPYING-2.0
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/MSNT/README.html helpers/doc/MSNT.README.html
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/MSNT/msntauth.conf.default helpers/doc/msntauth.conf.default
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/SASL/README helpers/doc/SASL.README
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/SASL/squid_sasl_auth helpers/doc/squid_sasl_auth
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/SASL/squid_sasl_auth.conf helpers/doc/squid_sasl_auth.conf
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/SMB/README helpers/doc/SASL.README
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/basic_auth/multi-domain-NTLM/README.txt helpers/doc/NTLM.README.txt
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/external_acl/ip_user/README helpers/doc/ip_user.README
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/external_acl/ip_user/example-deny_all_but.conf helpers/doc/ip_user.example-deny_all_but.conf
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/external_acl/ip_user/example.conf helpers/doc/ip_user.example.conf
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/external_acl/unix_group/README helpers/doc/unix_group.README
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/external_acl/winbind_group/readme.txt helpers/doc/winbind_group.readme.txt
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/external_acl/unix_group/README helpers/doc/unix_group.README
%__install -D -p -m644 $RPM_BUILD_DIR/%name-%version/helpers/ntlm_auth/no_check/README.no_check_ntlm_auth helpers/doc/README.no_check_ntlm_auth

%pre
/usr/sbin/groupadd -r -f %name >/dev/null 2>&1
/usr/sbin/useradd -r -n -g %name -d %_spooldir/%name -s /dev/null %name >/dev/null 2>&1 ||:

%__chown %name:%name %_logdir/%name/*.log >/dev/null 2>&1 ||:
%__chmod 660 %_logdir/%name/*.log >/dev/null 2>&1 ||:

%post
%post_service %name

%preun
%preun_service %name
%triggerpostun -- squid < 2.4.STABLE4-alt1
[ $2 -gt 0 ] || exit 0
%__chown -R %name:%name %_spooldir/%name >/dev/null 2>&1 ||:

%files
%doc faq/* README ChangeLog QUICKSTART doc/*
%doc scripts/*.pl helpers/doc/*

%config(noreplace) %_sysconfdir/%name/%name.conf
%config(noreplace) %_sysconfdir/%name/%name.conf.default
%config(noreplace) %_sysconfdir/%name/mime.conf
%config(noreplace) %_sysconfdir/%name/mime.conf.default
%config(noreplace) %_sysconfdir/%name/msntauth.conf
%config(noreplace) %_sysconfdir/%name/msntauth.conf.default

%config %_initdir/%name
%config %_sysconfdir/logrotate.d/%name

%_datadir/%name/errors
%_datadir/%name/icons
%_datadir/%name/mib.txt

%dir %_libdir/%name
%_libdir/%name/cachemgr.cgi
%_libdir/%name/digest_pw_auth
%_libdir/%name/diskd
%_libdir/%name/fakeauth_auth
%_libdir/%name/getpwname_auth
%_libdir/%name/ip_user_check
%_libdir/%name/msnt_auth
%_libdir/%name/ncsa_auth
%_libdir/%name/no_check.pl
%_libdir/%name/ntlm_auth
%_libdir/%name/pam_auth
%_libdir/%name/sasl_auth
%_libdir/%name/smb_auth
%_libdir/%name/smb_auth.sh
%_libdir/%name/smb_auth.pl
%_libdir/%name/squid_ldap_auth
%_libdir/%name/squid_ldap_group
%_libdir/%name/squid_unix_group
%_libdir/%name/unlinkd
%_libdir/%name/wb_auth
%_libdir/%name/wb_group
%_libdir/%name/wb_ntlmauth
%_libdir/%name/wbinfo_group.pl
%_libdir/%name/yp_auth

%_sbindir/%name
%_sbindir/squidclient
%_sbindir/RunAccel
%_sbindir/RunCache

%_man8dir/*

%attr(750,root,%name) %dir %_sysconfdir/%name
%attr(3770,root,%name) %dir %_logdir/%name
%attr(2770,root,%name) %dir %_spooldir/%name

%files pinger
%attr(4710,root,%name) %_libdir/%name/pinger

%changelog
* Thu Dec 09 2004 Denis Ovsienko <pilot@altlinux.ru> 2.5.STABLE7-alt4
- applied current patches:
 + 2004-12-08 01:03 (Minor) cachemgr vm_objects segfault
 + 2004-12-08 00:47 (Minor) httpd_accel_port 0 (virtual) not working correctly
 + 2004-12-07 23:45 (Cosmetic / Minor Security issue) Random error messages in response to malformed host name

* Sat Dec 04 2004 Denis Ovsienko <pilot@altlinux.ru> 2.5.STABLE7-alt3
- applied current patches:
 + 2004-11-07 23:37 (Minor) Squid fails to close TCP connection after blank HTTP response
 + 2004-11-06 21:42 (Minor) 100% CPU on startup on new/experimental Linux kernels due to O_NONBLOCK
 + 2004-11-06 15:28 (Minor) Failure to shut down busy helpers on -k rotate/reconfigure
 + 2004-10-20 23:23 (Minor) The new req_header and resp_header acls segfaults immediately on parse of squid.conf
 + 2004-10-19 10:09 (Cosmetic) Document -v (protocol version) option to LDAP helpers
 + 2004-10-14 22:48 (Minor) 100% CPU usage on half-closed PUT/POST requests

* Sun Nov 14 2004 Dmitry V. Levin <ldv@altlinux.org> 2.5.STABLE7-alt2
- Cleaned up build dependencies, was too superfluous
  since 2.5.STABLE6-alt1.
- Rebuilt with openldap-2.2.18-alt3.

* Tue Oct 12 2004 Denis Ovsienko <pilot@altlinux.ru> 2.5.STABLE7-alt1
- 2.5.STABLE7 (security fix)
- updated FAQ to 1.235 2004/10/04
- rediffed patches

* Sat Sep 04 2004 Denis Ovsienko <pilot@altlinux.ru> 2.5.STABLE6-alt3
- more patches

* Tue Aug 17 2004 Denis Ovsienko <pilot@altlinux.ru> 2.5.STABLE6-alt2
- Updated FAQ to 2004-08-10
- Added and rediffed official patches up to 2004-08-14
- build with 16384 file descriptors

* Fri Jul 23 2004 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE6-alt1
- 2.5.STABLE6
- Official bugfixes from www.%name-cache.org.
- add patch-aa.patch: makes squid write info in access.log by pieces as far as the
  receipt of data but not after downloading whole file. See -x options.

* Thu Jun 10 2004 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE5-alt4
- Official bugfixes from www.%name-cache.org.
- fix bugs id #4330

* Wed May 26 2004 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE5-alt3
- fix bugs id #1629

* Fri May 14 2004 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE5-alt2
- build with 8192 file descriptors
- Official bugfixes from www.%name-cache.org.

* Wed May 12 2004 ALT QA Team Robot <qa-robot@altlinux.org> 2.5.STABLE5-alt1.1
- Rebuilt with openssl-0.9.7d.

* Wed Mar 03 2004 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE5-alt1
- 2.5.STABLE5

* Thu Dec 18 2003 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE4-alt5
- fix build with libsasl2

* Mon Dec 08 2003 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE4-alt4
- Official bugfixes from www.%name-cache.org.
- cosmetics spec file

* Tue Nov 04 2003 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE4-alt3
- Fixed %%pre script.

* Tue Oct 21 2003 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE4-alt2
- Official bugfixes from www.%name-cache.org.
- disable default ICP setup.

* Fri Sep 26 2003 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE4-alt1
- 2.5.STABLE4

* Mon Jul 21 2003 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE3-alt3
- fix errors in squid init file.

* Mon Jul 14 2003 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE3-alt2
- Added Belarusian error pages by Vital Khilko (dojlid@mova.org)

* Fri Jul 11 2003 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE3-alt1
- 2.5.STABLE3
- fix bugs id #0002717
- Official bugfixes from www.%name-cache.org.
- Rewritten start/stop script to new rc scheme.

* Thu Nov 28 2002 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE1-alt5
- fix build support for the authentication schemes
- Official bugfixes from www.%name-cache.org.

* Mon Nov 25 2002 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE1-alt4
- fix documentations and manuals path

* Fri Nov 01 2002 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE1-alt3
- fix documentation

* Thu Oct 24 2002 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE1-alt2
- Fixed path on directories: %_var/run, %_logdir/%name and %_spooldir/%name.

* Tue Oct 22 2002 Konstantin Timoshenko <kt@altlinux.ru> 2.5.STABLE1-alt1
- 2.5.STABLE1
- misc adaptions

* Thu Aug 29 2002 Konstantin Timoshenko <kt@altlinux.ru> 2.4.STABLE7-alt4
- buildprereq autoconf = 2.13
- adding --enable-storeio

* Sun Jul 07 2002 Konstantin Timoshenko <kt@altlinux.ru> 2.4.STABLE7-alt3
- Official bugfixes from www.%name-cache.org.

* Thu Jul 04 2002 Stanislav Ievlev <inger@altlinux.ru> 2.4.STABLE7-alt2
- Relocated "chown" cleanup code from %%pre to %%triggerpostun (#1051).

* Wed Jul 03 2002 Konstantin Timoshenko <kt@altlinux.ru> 2.4.STABLE7-alt1
- 2.4.STABLE7

* Fri Jun 28 2002 Dmitry V. Levin <ldv@altlinux.org> 2.4.STABLE6-alt4
- Official bugfixes from www.%name-cache.org.

* Thu Jun 27 2002 Dmitry V. Levin <ldv@altlinux.org> 2.4.STABLE6-alt3
- Official bugfixes from www.%name-cache.org.

* Wed Apr 03 2002 Dmitry V. Levin <ldv@alt-linux.org> 2.4.STABLE6-alt2
- Build without bind-devel.

* Fri Mar 22 2002 Dmitry V. Levin <ldv@alt-linux.org> 2.4.STABLE6-alt1
- 2.4.STABLE6.

* Wed Mar 06 2002 Konstantin Timoshenko <kt@altlinux.ru> 2.4.STABLE4-alt2
- adding subpackage pinger.
- remove link to errors dir.

* Wed Feb 20 2002 Dmitry V. Levin <ldv@alt-linux.org> 2.4.STABLE4-alt1
- 2.4.STABLE4-alt1
- Fixed permissions on directories:
  %_sysconfdir/%name, %_libdir/%name, %_logdir/%name and %_spooldir/%name.

* Mon Feb 18 2002 Dmitry V. Levin <ldv@alt-linux.org> 2.4.STABLE3-alt2
- Added official patches for 2.4.STABLE3:
  + "htcp_port 0" fails to disable the HTCP port
  + Coredup on certain ftp:// style URL's
  + SNMP memory leaks
- Fixed %%pre script.

* Fri Feb 15 2002 Konstantin Timoshenko <kt@altlinux.ru> 2.4.STABLE3-alt1
- 2.4.STABLE3

* Mon Sep 24 2001 Kostya Timoshenko <kt@altlinux.ru> 2.4.STABLE2-alt1
- enable auth-modules LDAP, MSNT, NCSA, PAM, SMB, YP, getpwnam
- bugfix patches

* Mon Apr 16 2001 Kostya Timoshenko <kt@altlinux.ru> 2.4.STABLE1-ipl2mdk
- enable wccp, gnu-regex, cache-digests

* Mon Mar 26  2001 Kostya Timoshenko <kt@petr.kz> 2.4.STABLE1-ipl1mdk
- 2.4.STABLE1

* Mon Feb  5 2001 Kostya Timoshenko <kt@petr.kz> 2.3.STABLE4-ipl4mdk
- enable useragen log, icmp, async-io

* Wed Jan 17 2001 Kostya Timoshenko <kt@petr.kz>
- security fix for tmpfile problems (patch#20)

* Wed Jan  3 2001 Kostya Timoshenko <kt@petr.kz>
- fixed squid.init

* Wed Dec 27 2000 Kostya Timoshenko <kt@petr.kz>
- Rebuild for RE

* Sun Nov 12 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3.STABLE4-1mdk
- shiny version.
- comment out already applied patches.

* Tue Sep  5 2000 Etienne Faure  <etienne@mandraksoft.com> 2.3.STABLE2-3mdk
- rebuilt with %%doc macro
- added noreplace tag for config files

* Tue May  2 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.3.STABLE2-2mdk
- fixed %post script
- three more bugfix patches from the squid people
- buildprereq jade, sgmltools

* Fri Apr  7 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.3.STABLE2-1mdk
- merged with redhat again

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- make %pre more portable

* Thu Mar 16 2000 Bill Nottingham <notting@redhat.com>
- bugfix patches
- fix dependency on /usr/local/bin/perl

* Sat Mar  4 2000 Bill Nottingham <notting@redhat.com>
- 2.3.STABLE2

* Mon Feb 14 2000 Bill Nottingham <notting@redhat.com>
- Yet More Bugfix Patches

* Tue Feb  8 2000 Bill Nottingham <notting@redhat.com>
- add more bugfix patches
- --enable-heap-replacement

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- grab some bugfix patches

* Mon Jan 10 2000 Bill Nottingham <notting@redhat.com>
- 2.3.STABLE1 (whee, another serial number)

* Tue Dec 21 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix compliance with ftp RFCs
  (http://www.wu-ftpd.org/broken-clients.html)
- Work around a bug in some versions of autoconf
- BuildPrereq sgml-tools - we're using sgml2html

* Mon Oct 18 1999 Bill Nottingham <notting@redhat.com>
- add a couple of bugfix patches

* Wed Oct 13 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.STABLE5.
- update FAQ, fix URLs.

* Sat Sep 11 1999 Cristian Gafton <gafton@redhat.com>
- transform restart in reload and add restart to the init script

* Tue Aug 31 1999 Bill Nottingham <notting@redhat.com>
- add squid user as user 23.

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging
- fix conflict between logrotate & squid -k (#4562)

* Wed Jul 28 1999 Bill Nottingham <notting@redhat.com>
- put cachemgr.cgi back in /usr/lib/squid

* Wed Jul 14 1999 Bill Nottingham <notting@redhat.com>
- add webdav bugfix patch (#4027)

* Mon Jul 12 1999 Bill Nottingham <notting@redhat.com>
- fix path to config in squid.init (confuses linuxconf)

* Wed Jul  7 1999 Bill Nottingham <notting@redhat.com>
- 2.2.STABLE4

* Wed Jun 9 1999 Dale Lovelace <dale@redhat.com>
- logrotate changes
- errors from find when /var/spool/squid or
- /var/log/squid didn't exist

* Thu May 20 1999 Bill Nottingham <notting@redhat.com>
- 2.2.STABLE3

* Thu Apr 22 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.STABLE.2

* Sun Apr 18 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.STABLE1

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- don't need to run groupdel on remove
- fix useradd

* Mon Apr 12 1999 Bill Nottingham <notting@redhat.com>
- fix effective_user (bug #2124)

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- strip binaries

* Thu Apr  1 1999 Bill Nottingham <notting@redhat.com>
- duh. adduser does require a user name.
- add a serial number

* Tue Mar 30 1999 Bill Nottingham <notting@redhat.com>
- add an adduser in %pre, too

* Thu Mar 25 1999 Bill Nottingham <notting@redhat.com>
- oog. chkconfig must be in %preun, not %postun

* Wed Mar 24 1999 Bill Nottingham <notting@redhat.com>
- switch to using group squid
- turn off icmp (insecure)
- update to 2.2.DEVEL3
- build FAQ docs from source

* Tue Mar 23 1999 Bill Nottingham <notting@redhat.com>
- logrotate changes

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)

* Wed Feb 10 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.PRE2

* Wed Dec 30 1998 Bill Nottingham <notting@redhat.com>
- cache & log dirs shouldn't be world readable
- remove preun script (leave logs & cache @ uninstall)

* Tue Dec 29 1998 Bill Nottingham <notting@redhat.com>
- fix initscript to get cache_dir correct

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- update to 2.1.PATCH2
- merge in some changes from RHCN version

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- version 1.1.22

* Sun May 10 1998 Cristian Gafton <gafton@redhat.com>
- don't make packages conflict with each other...

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- added a proxy auth patch from Alex deVries <adevries@engsoc.carleton.ca>
- fixed initscripts

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- rebuilt for Manhattan

* Fri Mar 20 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.1.21/1.NOVM.21

* Mon Mar 02 1998 Cristian Gafton <gafton@redhat.com>
- updated the init script to use reconfigure option to restart squid instead
  of shutdown/restart (both safer and quicker)

* Sat Feb 07 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.1.20
- added the NOVM package and tryied to reduce the mess in the spec file

* Wed Jan 7 1998 Cristian Gafton <gafton@redhat.com>
- first build against glibc
- patched out the use of setresuid(), which is available only on kernels
  2.1.44 and later


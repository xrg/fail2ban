# spec file based on and patches graciously taken from tpg@mandriva
Summary:	Ban IP-addresses that result in too many password failures
Name:		fail2ban
Version:	0.8.13
Release:	%mkrel 2
License:	GPLv2+
Group:		System/Networking
URL:		http://www.fail2ban.org/
Source0:	https://codeload.github.com/%{name}/%{name}/tar.gz/%{version}
Source2:	%{name}.service
Source3:	%{name}.tmpfiles.conf
Patch0:		%{name}-0.8.13-jail-conf.patch
Patch3:		%{name}-0.8.13-log-actions-to-SYSLOG.patch
BuildRequires:	python-devel
BuildRequires:	systemd-units
Requires:	python		>= 2.5
Requires:	tcp_wrappers	>= 7.6-29
Requires:	iptables	>= 1.3.5-3
Requires:	syslog-daemon
Requires(post):	systemd >= %{systemd_required_version}
Requires(post):	rpm-helper >= 0.24.8-1
Requires(preun):rpm-helper >= 0.24.8-1
Requires(post):	systemd-units
Requires(preun):systemd-units
Suggests:	python-gamin
%py_requires -d
BuildArch:	noarch

%description
Fail2Ban scans log files like /var/log/secure and bans IP-addresses that have
too many password failures within a specified time frame. It updates firewall
rules to reject these IP addresses. The rules needed for this can be defined by
the user. Fail2Ban can read multiple log files including sshd and Apache web
server logs.

%prep
%setup -q
%patch0 -p0
%patch3 -p0

%build
%serverbuild
env CFLAGS="%{optflags}" python setup.py build 

pushd man
sh generate-man
popd

%install
python setup.py install --root=%{buildroot}

install -d %{buildroot}/%{_mandir}/man1
install man/*.1 %{buildroot}%{_mandir}/man1/
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%post
%_tmpfilescreate %{name}
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%doc ChangeLog README.md TODO
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf 
%{_bindir}/%{name}-*
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/action.d/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/filter.d/*.conf
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/action.d
%dir %{_sysconfdir}/%{name}/filter.d
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/client
%dir %{_datadir}/%{name}/server
%dir %{_datadir}/%{name}/common
%{_datadir}/%{name}/client/*.py*
%{_datadir}/%{name}/server/*.py*
%{_datadir}/%{name}/common/*.py*
%{_datadir}/%{name}/testcases/*.py*
%{_datadir}/%{name}/*-info
%{_mandir}/man1/*

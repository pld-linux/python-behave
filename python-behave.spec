#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Behaviour-driven development, Python style
Summary(pl.UTF-8):	Programowanie sterowane zachowaniem - w stylu Pythona
Name:		python-behave
Version:	1.2.6
Release:	9
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/behave/
Source0:	https://files.pythonhosted.org/packages/source/b/behave/behave-%{version}.tar.gz
# Source0-md5:	3f05c859a1c45f5ed33e925817ad887d
Patch0:		%{name}-mock.patch
Patch1:		behave-backport-for-py38-fixes.patch
Patch2:		behave-tweak-tests-required-by-pytest-5.0.patch
Patch3:		behave-invalid-escape-seq.patch
Patch4:		behave-sphinx-extlinks.patch
Patch5:		behave-drop_2to3.patch
URL:		https://pypi.org/project/behave/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-enum34
BuildRequires:	python-mock >= 2.0
BuildRequires:	python-nose >= 1.3
BuildRequires:	python-parse >= 1.8.2
BuildRequires:	python-parse_type >= 0.4.2
BuildRequires:	python-path >= 10.1
BuildRequires:	python-pyhamcrest >= 1.9
BuildRequires:	python-pytest >= 3.0
BuildRequires:	python-six >= 1.11
BuildRequires:	python-traceback2
%if "%{py_ver}" < "2.7"
BuildRequires:	python-argparse
BuildRequires:	python-importlib
BuildRequires:	python-ordereddict
%endif
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-nose >= 1.3
BuildRequires:	python3-parse >= 1.8.2
BuildRequires:	python3-parse_type >= 0.4.2
BuildRequires:	python3-path >= 10.1
BuildRequires:	python3-pyhamcrest >= 1.9
BuildRequires:	python3-pytest >= 3.0
BuildRequires:	python3-six >= 1.11
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_bootstrap_theme >= 0.6.0
BuildRequires:	sphinx-pdg-3 >= 1.6
%endif
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
behave is behavior-driven development, Python style.

%description -l pl.UTF-8
behave to programowanie sterowane zachowaniem, w stylu Pythona.

%package -n python3-behave
Summary:	Behaviour-driven development, Python style
Summary(pl.UTF-8):	Programowanie sterowane zachowaniem - w stylu Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-behave
behave is behavior-driven development, Python style.

%description -n python3-behave -l pl.UTF-8
behave to programowanie sterowane zachowaniem, w stylu Pythona.

%package apidocs
Summary:	API documentation for Python behave module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona behave
Group:		Documentation

%description apidocs
API documentation for Python behave module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona behave.

%prep
%setup -q -n behave-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
# can't get test_text__with_raised_exception_and_bytes_message test to work
# (LC_ALL=C.UTF-8 and PYTHONIOENCODING=utf-8 don't help)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests -k 'not test_text__with_raised_exception_and_bytes_message'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/lib \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{behave,behave-2}

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-behave-%{version}
# async_step requires python3.5+, don't install in python2 package
cp -pr examples/env_vars $RPM_BUILD_ROOT%{_examplesdir}/python-behave-%{version}

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{behave,behave-3}

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-behave-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-behave-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/behave-2
%{py_sitescriptdir}/behave
%{py_sitescriptdir}/behave-%{version}-py*.egg-info
%{py_sitescriptdir}/setuptools_behave.py[co]
%{_examplesdir}/python-behave-%{version}
%endif

%if %{with python3}
%files -n python3-behave
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/behave-3
%{py3_sitescriptdir}/behave
%{py3_sitescriptdir}/behave-%{version}-py*.egg-info
%{py3_sitescriptdir}/setuptools_behave.py
%{py3_sitescriptdir}/__pycache__/setuptools_behave.cpython-*.py[co]
%{_examplesdir}/python3-behave-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build/docs/html/{_images,_static,*.html,*.js}
%endif

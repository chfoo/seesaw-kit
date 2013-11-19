'''Miscellaneous functions.'''
import subprocess


def test_executable(name, version, path, version_arg="-V"):
    '''Try to run an executable and check its version.'''
    print "Looking for %s in %s" % (name, path)
    try:
        process = subprocess.Popen(
            [path, version_arg],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout_data, stderr_data = process.communicate()
        result = stdout_data + stderr_data
        if not process.returncode == 0:
            print "%s: Returned code %d" % (path, process.returncode)
            return False

        if isinstance(version, basestring):
            if not version in result:
                print "%s: Incorrect %s version (want %s)." % (path, name, version)
                return False
        elif hasattr(version, "search"):
            if not version.search(result):
                print "%s: Incorrect %s version." % (path, name)
                return False
        elif hasattr(version, "__iter__"):
            if not any((v in result) for v in version):
                print "%s: Incorrect %s version (want %s)." % (path, name, str(version))
                return False

        print "Found usable %s in %s" % (name, path)
        return True
    except OSError as e:
        print "%s:" % path, e
        return False


def find_executable(name, version, paths, version_arg="-V"):
    '''Returns the path of a matching executable.

    :seealso: :func:`test_executable`
    '''
    for path in paths:
        if test_executable(name, version, path, version_arg):
            return path
    return None

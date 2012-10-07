#     Copyright 2012, Kay Hayen, mailto:kayhayen@gmx.de
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Templates for raising exceptions, making assertions, and try/finally construct.

"""

try_except_template = """\
_frame_exception_keeper.preserveExistingException();
try
{
%(tried_code)s
}
catch ( _PythonException &_exception )
{
    if ( !_exception.hasTraceback() )
    {
        _exception.setTraceback( %(tb_making)s );
    }
    else if ( traceback == false )
    {
        _exception.addTraceback( frame_guard.getFrame() );
    }

#if PYTHON_VERSION > 300
    PythonExceptionStacker exception_restorer;
#endif

    _exception.toExceptionHandler();

    frame_guard.detachFrame();

%(exception_code)s
}"""


try_except_reraise_unmatched_template = """\
else
{
    traceback = true;
    throw;
}"""

try_finally_template = """\
_PythonExceptionKeeper _caught_%(try_count)d;
bool _continue_%(try_count)d = false;
bool _break_%(try_count)d = false;
bool _return_%(try_count)d = false;

try
{
%(tried_code)s
}
catch ( _PythonException &_exception )
{
    if ( !_exception.hasTraceback() )
    {
        _exception.setTraceback( %(tb_making)s );
    }
    else if ( traceback == false )
    {
        _exception.addTraceback( frame_guard.getFrame() );
    }
    traceback = true;

    _caught_%(try_count)d.save( _exception );

    frame_guard.detachFrame();
}
catch ( ContinueException & )
{
    _continue_%(try_count)d = true;
}
catch ( BreakException & )
{
    _break_%(try_count)d = true;
}
catch ( ReturnException & )
{
    _return_%(try_count)d = true;
}

// Final code:
%(final_code)s

_caught_%(try_count)d.rethrow();

if ( _continue_%(try_count)d )
{
    throw ContinueException();
}
if ( _break_%(try_count)d )
{
    throw BreakException();
}
if ( _return_%(try_count)d )
{
    throw ReturnException();
}"""

frame_exceptionkeeper_setup = """\
FrameExceptionKeeper _frame_exception_keeper;"""

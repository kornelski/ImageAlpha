//
//  main.m
//  ImageAlpha

#import <Python/Python.h>
#import <Cocoa/Cocoa.h>

int main(int argc, char *argv[])
{
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];

    NSBundle *mainBundle = [NSBundle mainBundle];
    NSString *resourcePath = [mainBundle resourcePath];
    NSArray *pythonPathArray = [NSArray arrayWithObjects: resourcePath, [resourcePath stringByAppendingPathComponent:@"PyObjC"], nil];

    setenv("PYTHONPATH", [[pythonPathArray componentsJoinedByString:@":"] UTF8String], 1);

    NSArray *possibleMainExtensions = [NSArray arrayWithObjects: @"py", @"pyc", @"pyo", nil];
    NSString *mainFilePath = nil;

    for (NSString *possibleMainExtension in possibleMainExtensions) {
        mainFilePath = [mainBundle pathForResource: @"main" ofType: possibleMainExtension];
        if ( mainFilePath != nil ) break;
    }

    int result = -1;
	if ( mainFilePath ) {

        Py_SetProgramName("/usr/bin/python");
        Py_Initialize();
        PySys_SetArgv(argc, (char **)argv);

        const char *mainFilePathPtr = [mainFilePath fileSystemRepresentation];
        FILE *mainFile = fopen(mainFilePathPtr, "r");
        result = PyRun_SimpleFile(mainFile, (char *)[[mainFilePath lastPathComponent] UTF8String]);

    }
    if ( result != 0 ) {
        NSAlert *alert = [NSAlert alertWithMessageText:@"Unable to start ImageAlpha" defaultButton:@"Abort" alternateButton:nil otherButton:nil
                             informativeTextWithFormat:@"Python/PyObjC program failed to start.\nSee Console.app for details.",nil];
        [alert runModal];
    }

    [pool drain];

    return result;
}

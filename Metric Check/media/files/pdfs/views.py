from django.db import models
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
import pyrebase
from radon.visitors import ComplexityVisitor, HalsteadVisitor
from radon.complexity import cc_rank, cc_visit, cc_visit_ast
from radon.metrics import h_visit, mi_visit, mi_rank, mi_parameters, mi_compute, h_visit_ast
from radon.raw import analyze
from Metrics.forms import userForm, UploadfileForm
from Metrics.models import *
from datetime import *
import re
from msilib.schema import File
from random import randint
from django.conf import settings
from django.contrib import messages
import os
import ast
import sys
from math import log2
import math
import time
# from metricbase import MetricBase
import token
import tokenize
import lizard


# our token types
KEYWORD     = token.NT_OFFSET + 1
TEXT        = token.NT_OFFSET + 2
WS          = token.NT_OFFSET + 3
DOCSTRING   = token.NT_OFFSET + 4
VARNAME     = token.NT_OFFSET + 5
CLASSNAME   = token.NT_OFFSET + 6
FCNNAME     = token.NT_OFFSET + 7
INLINE      = token.NT_OFFSET + 8
UNKNOWN     = token.NT_OFFSET + 9
SEMTOKEN    = token.NT_OFFSET + 10  # to distinguish semantic tokens
NONTOKEN    = token.NT_OFFSET + 11  # to distinguish non-tokens
DECORATOR   = token.NT_OFFSET + 12  # to indicate decorator token
NUMBER      = token.NUMBER
OP          = token.OP
STRING      = token.STRING
COMMENT     = tokenize.COMMENT
NAME        = token.NAME
ERRORTOKEN  = token.ERRORTOKEN
ENDMARKER   = token.ENDMARKER
INDENT      = token.INDENT
DEDENT      = token.DEDENT
NEWLINE     = token.NEWLINE
EMPTY       = tokenize.NL

# new token types added to allow for character representation of new codes

token.tok_name[KEYWORD] = "KEYWORD"     # one of Python's reserved words
token.tok_name[TEXT] = "TEXT"           # obsolete - but kept for compatibility
token.tok_name[WS] = "WS"               # some form of whitespace
token.tok_name[DOCSTRING] = "DOCSTRING" # literal that is also doc string
token.tok_name[VARNAME] = "VARNAME"     # name that is not keyword
token.tok_name[CLASSNAME] = "CLASSNAME" # name defined in class statment
token.tok_name[FCNNAME] = "FCNNAME"     # name defined in def statement
token.tok_name[INLINE] = "INLINE"       # comment that follows other text on same line
token.tok_name[UNKNOWN] = "UNKNOWN"     # Unknown semantic type - this should not occur
token.tok_name[DECORATOR] = 'DECORATOR' # Decorator marker



class MetricBase( object ):
    """ Metric template class."""
    def __init__( self, *args, **kwds ):
        pass
        
    def processSrcLines( self, srcLines, *args, **kwds ):
        """ Handle physical line after tab expansion."""
        pass
        
    def processToken( self, fcnName, className, tok, *args, **kwds ):
        """ Handle processing after each token processed."""
        pass
        
    def processStmt( self, fcnName, className, stmt, *args, **kwds ):
        """ Handle processing at end of statement."""
        pass
        
    def processBlock( self, fcnName, className, block, *args, **kwds ):
        """ Handle processing at end of block."""
        pass
        
    def processFunction( self, fcnName, className, fcn, *args, **kwds ):
        """ Handle processing at end of function. """
        pass
        
    def processClass( self, fcnName, className, cls, *args, **kwds ):
        """ Handle processing at end of class. """
        pass
        
    def processModule( self, moduleName, module, *args, **kwds ):
        """ Handle processing at end of module. """
        pass
        
    def processRun( self, run, *args, **kwds ):
        """ Handle processing at end of run. """
        pass

    def compute( self, *args, **kwds ):
        """ Compute the metric given all needed info known."""
        pass
        
class HalsteadMetric( MetricBase ):
    """ Compute various HalsteadMetric metrics. """
    totalV = 0
    totalE = 0
    numModules = 0
    def __init__( self, context, runMetrics, metrics, pa, *args, **kwds ):
        """ Initialization for the HalsteadMetric metrics."""
        self.inFile = context['inFile']
        self.context = context
        self.runMetrics = runMetrics
        self.metrics = metrics
        self.pa = pa
        self.inFile = context['inFile']
        self.numOperators = 0
        self.numOperands = 0
        self.uniqueOperators = {}
        self.uniqueOperands = {}
        HalsteadMetric.numModules += 1
        
        # initialize category accummulators as dictionaries
        self.hsDict = {}
        for t in ['token','stmt','block','function','class','module','run']:
            self.uniqueOperators[t] = {}
            self.uniqueOperands[t] = {}
            #for v in ['N','N1','N2','n','n1','n2','V','D','E','avgV','avgE']:
            #    self.hsDict[(t,v)] = 0
        
    def processToken( self, currentFcn, currentClass, tok, *args, **kwds ):
        """ Collect token data for Halstead metrics."""
        if tok.type in [WS, EMPTY, ENDMARKER, NEWLINE, EMPTY, COMMENT]:
            pass
        elif tok.type in [OP, INDENT, DEDENT]:
            self.numOperators += 1
            self.uniqueOperators['token'][tok.text] = self.uniqueOperators['token'].get(tok.text, 0) + 1
        else:
            self.numOperands += 1
            sDict = self.context.__repr__()
            k = (sDict,tok.text)
            self.uniqueOperands['token'][k] = self.uniqueOperands['token'].get(tok.text, 0) + 1

    def processStmt( self, currentFcn, currentClass, stmt, *args, **kwds ):
        """ Collect statement data for Halstead metrics."""
        
        result = None
        
        # the two lines following this comment would compute the Halstead 
        # metrics for each statement in the run, However, it is 
        # normally overkill, so these lines are commented out.
        
        #lineNum = stmt[0].row
        #result = self.computeCategory( 'stmt', lineNum, stmt )
        
        return result
        
    def processBlock( self, currentFcn, currentClass, block, *args, **kwds ):
        """ Collect block data for Halstead metrics."""

        result = None

        # the two lines following this comment would compute the Halstead 
        # metrics for each statement in the run, However, it is 
        # normally overkill, so the two lines are commented out.
        
        #blockNum = self.context['blockNum']
        #result = self.computeCategory( 'block', blockNum, block )
        
        return result

    def processFunction( self, currentFcn, currentClass, fcn, *args, **kwds ):
        """ Collect function data for Halstead metrics."""
        result = self.computeCategory( 'function', currentFcn, fcn )
        return result
        
    def processClass( self, currentFcn, currentClass, cls, *args, **kwds ):
        """ Collect class data for Halstead metrics."""
        result = self.computeCategory( 'class', currentClass, cls )
        return result
        
    def processModule( self, moduleName, mod, *args, **kwds ):
        """ Collect module data for Halstead metrics."""
        result = self.computeCategory( 'module', moduleName, mod )
        return result
        
    def processRun( self, run, *args, **kwds ):
        """ Collect run data for Halstead metrics."""
        datestamp = time.strftime("%Y-%m-%d.%H:%m%Z",time.localtime())
        result = self.computeCategory( 'run', datestamp, run )
        return result
        
    def __LOGb( self, x, b ): 
        """ convert to LOGb(x) from natural logs."""
        try:
            result = math.log( x ) / math.log ( b )
        except OverflowError:
            result = 1.0
        return result

    def computeIncr( self, cat, tok, uniqueOperators, uniqueOperands ):
        """ Compute increment for token depending on which category it falls into."""
        operatorIncr = operandIncr = 0
        if tok.type in [WS, EMPTY, ENDMARKER, NEWLINE, EMPTY, COMMENT]:
            return (operatorIncr,operandIncr)
            
        if tok.type in [OP, INDENT, DEDENT]:
            operatorIncr = 1
            uniqueOperators[tok.text] = uniqueOperators.get(tok.text, 0) + 1
        else:
            operandIncr = 1
            uniqueOperands[tok.text] = uniqueOperands.get(tok.text,0) + 1
            
        return (operatorIncr,operandIncr)
        
    def computeCategory( self, cat, mod, lst ):
        """ Collection data for cat of code."""
        modID= id( mod )
        numOperators = numOperands = 0
        for tok in lst:
            result = self.computeIncr( cat, tok, self.uniqueOperators[cat], self.uniqueOperands[cat] )
            numOperators += result[0]
            numOperands += result[1]
        result = self.compute( cat, modID, numOperators, numOperands, self.uniqueOperators[cat], self.uniqueOperands[cat] )
        return result
        
    def compute( self, cat, modID, numOperators, numOperands, uniqueOperators, uniqueOperands, *args, **kwds ):
        """ Do actual calculations here."""
        
        n1 = len( uniqueOperands )
        n2 = len( uniqueOperators )
        N1 = numOperands
        N2 = numOperators
        N = N1 + N2
        n = n1 + n2
        V = float(N) * self.__LOGb( n, 2 )
        try:
            D = (float(n1)/2.0) * (float(N2)/float(n2))
        except ZeroDivisionError:
            D = 0.0
        E = D * V
        HalsteadMetric.totalV += V
        HalsteadMetric.totalE += E
        avgV = HalsteadMetric.totalV / HalsteadMetric.numModules
        avgE = HalsteadMetric.totalE / HalsteadMetric.numModules
        
        self.hsDict[(cat,modID,'n1')] = n1
        self.hsDict[(cat,modID,'n2')] = n2
        self.hsDict[(cat,modID,'N1')] = N1
        self.hsDict[(cat,modID,'N2')] = N2
        self.hsDict[(cat,modID,'N')] = N
        self.hsDict[(cat,modID,'n')] = n
        self.hsDict[(cat,modID,'V')] = V
        self.hsDict[(cat,modID,'D')] = D
        self.hsDict[(cat,modID,'E')] = E
        self.hsDict[(cat,modID,'numModules')] = HalsteadMetric.numModules
        self.hsDict[(cat,modID,'avgV')] = avgV
        self.hsDict[(cat,modID,'avgE')] = avgE
        
        return self.hsDict
        
    def display( self, cat=None ):
        """ Display the computed Halstead Metrics."""
        if self.pa.quietSw:
            return self.hsDict
            
        hdr = "\nHalstead Metrics for %s" % self.inFile
        print(hdr)
        print("-"*len(hdr) + '\n')
        
        if len( self.hsDict ) == 0:
            print ("%-8s %-30s " % ('**N/A**','All Halstead metrics are zero'))
            return self.hsDict
            
        keyList = self.hsDict.keys()
        keyList.sort()
        if 0:
            for k,i,v in keyList:
                if cat:
                    if k!=cat:
                        continue
                print("%14.2f %s %s %s" % (self.hsDict[(k,i,v)],k,i,v) )
            print( hdr1 = "Category Identifier                                D        E     N   N1   N2        V     avgE     avgV     n   n1   n2",
        hdr2 = "-------- ---------------------------------- -------- -------- ----- ---- ---- -------- -------- -------- ----- ---- ----")
        #       12345678 123456789012345678901234567890  12345678 12345678 12345 1234 1234 12345678 12345678 12345678 12345 1234 1234
        fmt1 = "%-8s %-33s "
        fmt2 = "%8.2e %8.2e %5d %4d %4d %8.2e %8.2e %8.2e %5d %4d %4d"
        
        # this loop uses the Main Line Standards break logic. It does this to convert the
        # normal vertical output to a horizontal format. The control variables are the
        # category name and the identifier value.
        
        oldK = oldI = None
        vDict = {}
        vList = []
        hdrSw = True                # output header for first time thru
        for k,i,v in keyList:
            # only print data for the category we want
            if cat:
                if k != cat:
                    continue 
                    
            if v == "numModules":    # ignore this value for now
                continue
                
            if (oldK,oldI) != (k,i):    # change in category/id
                if oldK and oldI:           # this is not first time thru
                    #t = tuple([self.hsDict[(k,i,v)] for v in vList])
                    t = tuple([vDict[v] for v in vList])
                    print(fmt1 % (k,i))
                    print (fmt2 % t)
                # initialize for next set of category/id
                vDict = {}
                vDict[v] = self.hsDict[(k,i,v)]
                vList = []
                vList.append( v )
                oldK = k
                oldI = i
                if hdrSw:
                    print(hdr1)
                    print(hdr2)
                    hdrSw = False
            else:       # we are still in the same category/id
                vDict[v] = self.hsDict[(k,i,v)]
                vList.append( v )

        print
                
        return self.hsDict
        
# config ={
    # 'apiKey': "AIzaSyDNby6i5an-cHNGKznfWnezOeCkjBKa2Z0",
    # 'authDomain': "metric-check.firebaseapp.com",
    # 'databaseURL': "https://metric-check.firebaseio.com",
    # 'projectId': "metric-check",
    # 'storageBucket': "metric-check.appspot.com",
    # 'messagingSenderId': "290870343358",
    # 'appId': "1:290870343358:web:5133d8f5d7731c15aa10ef",
    # 'measurementId': "G-CLN4EZNDFZ"
# }
# # firebase.initializeApp(config);
# firebase = pyrebase.initialize_app(config)

# auth = firebase.auth()

# def signin(request):
    # return render(request, 'user/new/signin.html')

# def postsignin(request):
    # return render(request, 'user/new/postsignin.html')


# ---------------------------------------------------
# ---------------------------------------------------
def index(request):
    return render(request, 'index.html')

def adminpage(request):
    return render(request, 'admin/adminpage.html')

def hai(request):
    return render(request, 'user/hai.html')

def userpage(request):
    return render(request, "user/userpage.html")

def adminlogin(request):
    return render(request, "admin/adminlogin.html")

def adminloginentered(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        passwd=request.POST['upass']
        if uname == 'admin' and passwd=='sadaf':
            return render(request,"admin/adminloginentered.html")
        else:

            return render(request, "admin/adminlogin.html")


def logout(request):
    return render(request,'index.html')


def userlogin(request):
    return render(request,"user/userlogin.html")

def userregister(request):
    if request.method=='POST':
        form1=userForm(request.POST)
        if form1.is_valid():
            form1.save()
            return render(request, "user/userlogin.html")
            #return HttpResponse("registration succesfully completed")
        else:
            print("form not valid")
            return HttpResponse("form not valid")
    else:
        form=userForm()
        return render(request,"user/userregister.html",{"form":form})

def viewuserdata(request):
    s=user.objects.all()
    return render(request,"admin/viewuserdata.html",{"qs":s})

def userdeactivate(request):
    # print("hello gud evng")
    id=request.GET.get('pid')
    print("id",id)
    user.objects.filter(id=id).delete()
    qs = user.objects.all()
    return render(request,"admin/viewuserdata.html",{"qs": qs})

def activateuser(request):
    if request.method == 'GET':
        uname=request.GET.get('pid')
        print(uname)
        status='Activated'
        print("pid=",uname,"status=",status)
        user.objects.filter(id=uname).update(status=status)
        qs=user.objects.all()
        return render(request,"admin/viewuserdata.html",{"qs":qs})


def userlogincheck1(request):
    if request.method == 'POST':
        uname = request.POST.get('umail')
        print(uname)
        upasswd = request.POST.get('upasswd')
        print(upasswd)
        try:
            check = user.objects.get(mail=uname, passwd=upasswd)
            # print('usid',usid,'pswd',pswd)
            print(check)
            request.session['name'] = check.name
            # print("name",check.name)
            status = check.status
            print('status',status)
            if status == "Activated":
                request.session['mail'] = check.mail
                return render(request, 'user/userpage.html')
            else:
                messages.success(request, 'user is not activated')
                return render(request, 'user/userlogin.html')
        except Exception as e:
            print('Exception is ',str(e))
            pass
        messages.success(request,'Invalid Email id and password')
        return render(request,'user/userlogin.html')

def problems(request):
    return render(request, "user/problems.html")


def uploadfile(request):
    if request.method == 'POST':
        form = UploadfileForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user/upload_list.html')
    else:
        form = UploadfileForm()
    return render(request, 'user/uploadfile.html', {'form': form})

def upload_list(request):
    files = File.objects.all()
    return render(request, 'user/upload_list.html', {'files': files})
    

    
    id=request.GET.get('pid')
    
    user.objects.filter(id=id).delete()
    filedata = user.objects.all()
    return render(request,"user/viewfildata.html",{"object": filedata})

def viewfile(request):
    id=request.session['name']
    filedata = upload.objects.all()
    return render(request, 'admin/viewfiles.html', {'object': filedata})

def viewfildata(request):
    filedata = upload.objects.all()
    return render(request, 'user/viewfiledata.html', {'object': filedata})

def userviewfildata(request):
    id = request.session['name']
    print("id",id)
    filedata = upload.objects.filter(upldrname=id)
    print("filedata",filedata)
    return render(request, 'user/viewfiledata.html',{'object':filedata})



# def userfiledata(request):
#     if request.method == "GET":
#         file = request.GET.get('id')
#         try:
#             print("file", file)
#             head, fileName = os.path.split(file)
#
#             fPath = settings.MEDIA_ROOT + '\\' + 'files\pdfs' + '\\' + fileName
#
#             f = open(fPath)
#             loc = 0
#             wordcount = 0
#             chrcount = 0
#             cmntcount = 0
#             classcount = 0
#             for line in f:
#                 loc = loc + 1
#                 chrcount = chrcount + len(line)
#                 word = line.split(' ')
#                 wordcount = wordcount + len(word)
#                 if line.startswith('#'):
#                     cmntcount = cmntcount + 1
#                 if line.startswith('class'):
#                     classcount = classcount + 1
#             f = open(fPath)
#             fd = f.read()
#             stats = os.stat(fPath)
#             s = datetime.fromtimestamp(stats.st_atime)
#             s1 = datetime.fromtimestamp(stats.st_mtime)
#             size1 = stats.st_size
#             print("file size in bytes:", size1)
#             print('class-count', classcount)
#             with open(fPath) as f:
#                 tree = ast.parse(f.read())
#                 func = sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)
#             '''it's about finding condintion statements and loops'''
#             f = open(fPath)
#             lpcountif = lpcountelif = lpcountelse = lpcountfor = 0
#             line = f.readlines()
#             for x in line:
#                 if re.search('if ', x):
#                     lpcountif = lpcountif + 1
#                 if re.search('elif ', x):
#                     lpcountelif = lpcountelif + 1
#                 if re.search('else ', x):
#                     lpcountelse = lpcountelse + 1
#                 if re.search('for ', x):
#                     lpcountfor = lpcountfor + 1
#             cmplx = lpcountif + lpcountelif + lpcountelse + lpcountfor
#             if cmplx <= 10:
#                 perfrmance = "normal"
#             elif cmplx > 10 and cmplx <= 20:
#                 perfrmance = "moderate"
#             else:
#                 perfrmance = "high"
#
#
#             message = {"filename": f.name, "lines": loc, "words": wordcount, "charecters": chrcount, "content": fd,
#                        "functionscount": func, "commentlinescount": cmntcount, "lastmodifiedtime": s1,
#                        "lastaccessedtime": s, "classescount": classcount, "ifloop": lpcountif, "elifloop": lpcountelif,
#                        "elseloop": lpcountelse,"filesize":size1, "forloop": lpcountfor,"cmplx":cmplx,"perf":perfrmance}
#             return render(request, "user/userfiledata.html", {"message": message})
#         except Exception as e:
#             print('Exception is ', str(e))
#             messages.success(request, 'Invalid Details')
#         return render(request, 'user/userfiledata.html')

def userfiledata(request):
    if request.method == "GET":
        file = request.GET.get('id')
        try:

            print("file", file)
            head, fileName = os.path.split(file)
            fPath = settings.MEDIA_ROOT + '\\' + 'files\pdfs' + '\\' + fileName
            f =open(fPath)
            
            class MetricBase( object ):
                """ Metric template class."""
                def __init__( self, *args, **kwds ):
                    pass
                    
                def processSrcLines( self, srcLines, *args, **kwds ):
                    """ Handle physical line after tab expansion."""
                    pass
                    
                def processToken( self, fcnName, className, tok, *args, **kwds ):
                    """ Handle processing after each token processed."""
                    pass
                    
                def processStmt( self, fcnName, className, stmt, *args, **kwds ):
                    """ Handle processing at end of statement."""
                    pass
                    
                def processBlock( self, fcnName, className, block, *args, **kwds ):
                    """ Handle processing at end of block."""
                    pass
                    
                def processFunction( self, fcnName, className, fcn, *args, **kwds ):
                    """ Handle processing at end of function. """
                    pass
                    
                def processClass( self, fcnName, className, cls, *args, **kwds ):
                    """ Handle processing at end of class. """
                    pass
                    
                def processModule( self, moduleName, module, *args, **kwds ):
                    """ Handle processing at end of module. """
                    pass
                    
                def processRun( self, run, *args, **kwds ):
                    """ Handle processing at end of run. """
                    pass

                def compute( self, *args, **kwds ):
                    """ Compute the metric given all needed info known."""
                    pass
                    
            class HalsteadMetric( MetricBase ):
                """ Compute various HalsteadMetric metrics. """
                totalV = 0
                totalE = 0
                numModules = 0
                def __init__( self, context, runMetrics, metrics, pa, *args, **kwds ):
                    """ Initialization for the HalsteadMetric metrics."""
                    self.inFile = context['inFile']
                    self.context = context
                    self.runMetrics = runMetrics
                    self.metrics = metrics
                    self.pa = pa
                    self.inFile = context['inFile']
                    self.numOperators = 0
                    self.numOperands = 0
                    self.uniqueOperators = {}
                    self.uniqueOperands = {}
                    HalsteadMetric.numModules += 1
                    
                    # initialize category accummulators as dictionaries
                    self.hsDict = {}
                    for t in ['token','stmt','block','function','class','module','run']:
                        self.uniqueOperators[t] = {}
                        self.uniqueOperands[t] = {}
                        #for v in ['N','N1','N2','n','n1','n2','V','D','E','avgV','avgE']:
                        #    self.hsDict[(t,v)] = 0
                    
                def processToken( self, currentFcn, currentClass, tok, *args, **kwds ):
                    """ Collect token data for Halstead metrics."""
                    if tok.type in [WS, EMPTY, ENDMARKER, NEWLINE, EMPTY, COMMENT]:
                        pass
                    elif tok.type in [OP, INDENT, DEDENT]:
                        self.numOperators += 1
                        self.uniqueOperators['token'][tok.text] = self.uniqueOperators['token'].get(tok.text, 0) + 1
                    else:
                        self.numOperands += 1
                        sDict = self.context.__repr__()
                        k = (sDict,tok.text)
                        self.uniqueOperands['token'][k] = self.uniqueOperands['token'].get(tok.text, 0) + 1

                def processStmt( self, currentFcn, currentClass, stmt, *args, **kwds ):
                    """ Collect statement data for Halstead metrics."""
                    
                    result = None
                    
                    # the two lines following this comment would compute the Halstead 
                    # metrics for each statement in the run, However, it is 
                    # normally overkill, so these lines are commented out.
                    
                    #lineNum = stmt[0].row
                    #result = self.computeCategory( 'stmt', lineNum, stmt )
                    
                    return result
                    
                def processBlock( self, currentFcn, currentClass, block, *args, **kwds ):
                    """ Collect block data for Halstead metrics."""

                    result = None

                    # the two lines following this comment would compute the Halstead 
                    # metrics for each statement in the run, However, it is 
                    # normally overkill, so the two lines are commented out.
                    
                    #blockNum = self.context['blockNum']
                    #result = self.computeCategory( 'block', blockNum, block )
                    
                    return result

                def processFunction( self, currentFcn, currentClass, fcn, *args, **kwds ):
                    """ Collect function data for Halstead metrics."""
                    result = self.computeCategory( 'function', currentFcn, fcn )
                    return result
                    
                def processClass( self, currentFcn, currentClass, cls, *args, **kwds ):
                    """ Collect class data for Halstead metrics."""
                    result = self.computeCategory( 'class', currentClass, cls )
                    return result
                    
                def processModule( self, moduleName, mod, *args, **kwds ):
                    """ Collect module data for Halstead metrics."""
                    result = self.computeCategory( 'module', moduleName, mod )
                    return result
                    
                def processRun( self, run, *args, **kwds ):
                    """ Collect run data for Halstead metrics."""
                    datestamp = time.strftime("%Y-%m-%d.%H:%m%Z",time.localtime())
                    result = self.computeCategory( 'run', datestamp, run )
                    return result
                    
                def __LOGb( self, x, b ): 
                    """ convert to LOGb(x) from natural logs."""
                    try:
                        result = math.log( x ) / math.log ( b )
                    except OverflowError:
                        result = 1.0
                    return result

                def computeIncr( self, cat, tok, uniqueOperators, uniqueOperands ):
                    """ Compute increment for token depending on which category it falls into."""
                    operatorIncr = operandIncr = 0
                    if tok.type in [WS, EMPTY, ENDMARKER, NEWLINE, EMPTY, COMMENT]:
                        return (operatorIncr,operandIncr)
                        
                    if tok.type in [OP, INDENT, DEDENT]:
                        operatorIncr = 1
                        uniqueOperators[tok.text] = uniqueOperators.get(tok.text, 0) + 1
                    else:
                        operandIncr = 1
                        uniqueOperands[tok.text] = uniqueOperands.get(tok.text,0) + 1
                        
                    return (operatorIncr,operandIncr)
                    
                def computeCategory( self, cat, mod, lst ):
                    """ Collection data for cat of code."""
                    modID= id( mod )
                    numOperators = numOperands = 0
                    for tok in lst:
                        result = self.computeIncr( cat, tok, self.uniqueOperators[cat], self.uniqueOperands[cat] )
                        numOperators += result[0]
                        numOperands += result[1]
                    result = self.compute( cat, modID, numOperators, numOperands, self.uniqueOperators[cat], self.uniqueOperands[cat] )
                    return result
                    
                def compute( self, cat, modID, numOperators, numOperands, uniqueOperators, uniqueOperands, *args, **kwds ):
                    """ Do actual calculations here."""
                    
                    n1 = len( uniqueOperands )
                    n2 = len( uniqueOperators )
                    N1 = numOperands
                    N2 = numOperators
                    N = N1 + N2
                    n = n1 + n2
                    V = float(N) * self.__LOGb( n, 2 )
                    try:
                        D = (float(n1)/2.0) * (float(N2)/float(n2))
                    except ZeroDivisionError:
                        D = 0.0
                    E = D * V
                    HalsteadMetric.totalV += V
                    HalsteadMetric.totalE += E
                    avgV = HalsteadMetric.totalV / HalsteadMetric.numModules
                    avgE = HalsteadMetric.totalE / HalsteadMetric.numModules
                    
                    self.hsDict[(cat,modID,'n1')] = n1
                    self.hsDict[(cat,modID,'n2')] = n2
                    self.hsDict[(cat,modID,'N1')] = N1
                    self.hsDict[(cat,modID,'N2')] = N2
                    self.hsDict[(cat,modID,'N')] = N
                    self.hsDict[(cat,modID,'n')] = n
                    self.hsDict[(cat,modID,'V')] = V
                    self.hsDict[(cat,modID,'D')] = D
                    self.hsDict[(cat,modID,'E')] = E
                    self.hsDict[(cat,modID,'numModules')] = HalsteadMetric.numModules
                    self.hsDict[(cat,modID,'avgV')] = avgV
                    self.hsDict[(cat,modID,'avgE')] = avgE
                    
                    return self.hsDict
                    
                def display( self, cat=None ):
                    """ Display the computed Halstead Metrics."""
                    if self.pa.quietSw:
                        return self.hsDict
                        
                    hdr = "\nHalstead Metrics for %s" % self.inFile
                    print(hdr)
                    print("-"*len(hdr) + '\n')
                    
                    if len( self.hsDict ) == 0:
                        print ("%-8s %-30s " % ('**N/A**','All Halstead metrics are zero'))
                        return self.hsDict
                        
                    keyList = self.hsDict.keys()
                    keyList.sort()
                    if 0:
                        for k,i,v in keyList:
                            if cat:
                                if k!=cat:
                                    continue
                            print("%14.2f %s %s %s" % (self.hsDict[(k,i,v)],k,i,v) )
                        print( hdr1 = "Category Identifier                                D        E     N   N1   N2        V     avgE     avgV     n   n1   n2",
                    hdr2 = "-------- ---------------------------------- -------- -------- ----- ---- ---- -------- -------- -------- ----- ---- ----")
                    #       12345678 123456789012345678901234567890  12345678 12345678 12345 1234 1234 12345678 12345678 12345678 12345 1234 1234
                    fmt1 = "%-8s %-33s "
                    fmt2 = "%8.2e %8.2e %5d %4d %4d %8.2e %8.2e %8.2e %5d %4d %4d"
                    
                    # this loop uses the Main Line Standards break logic. It does this to convert the
                    # normal vertical output to a horizontal format. The control variables are the
                    # category name and the identifier value.
                    
                    oldK = oldI = None
                    vDict = {}
                    vList = []
                    hdrSw = True                # output header for first time thru
                    for k,i,v in keyList:
                        # only print data for the category we want
                        if cat:
                            if k != cat:
                                continue 
                                
                        if v == "numModules":    # ignore this value for now
                            continue
                            
                        if (oldK,oldI) != (k,i):    # change in category/id
                            if oldK and oldI:           # this is not first time thru
                                #t = tuple([self.hsDict[(k,i,v)] for v in vList])
                                t = tuple([vDict[v] for v in vList])
                                print(fmt1 % (k,i))
                                print (fmt2 % t)
                            # initialize for next set of category/id
                            vDict = {}
                            vDict[v] = self.hsDict[(k,i,v)]
                            vList = []
                            vList.append( v )
                            oldK = k
                            oldI = i
                            if hdrSw:
                                print(hdr1)
                                print(hdr2)
                                hdrSw = False
                        else:       # we are still in the same category/id
                            vDict[v] = self.hsDict[(k,i,v)]
                            vList.append( v )

                    print
                            
                    return self.hsDict
                McCabeKeywords = {
                'assert':0,
                'break':1,
                'continue':1,
                'elif':1,
                'else':1,
                'for':1,
                'if':1,
                'while':1
                }
                
            class McCabeMetric( MetricBase ):
                """ Compute McCabe's Cyclomatic McCabeMetric by function."""
                def __init__( self, context, runMetrics, metrics, pa, *args, **kwds ):
                    self.context = context
                    self.runMetrics = runMetrics
                    self.metrics = metrics
                    self.pa = pa
                    self.inFile = context['inFile']
                    self.fcnNames = {}
                            
                def processToken( self, fcnName, className, tok, *args, **kwds ):
                    """ Increment number of decision points in function."""
                    if tok and tok.text in McCabeKeywords:
                        self.fcnNames[fcnName] = self.fcnNames.get(fcnName,0) + 1
                
                def processFunction( self, fcnName, className, fcn, *args, **kwds ):
                    """ Increment number of decision points in function."""
                    self.fcnNames[fcnName] = self.fcnNames.get(fcnName,0) + 1
                
                def display( self ):
                    """ Display McCabe Cyclomatic metric for each function """
                    result = {}
                    # the next three lines ensure that fcnNames[None] is treated
                    # like fcnNames['__main__'] and are sorted into alphabetical
                    # order.
                    if self.fcnNames.has_key(None):
                        self.fcnNames['__main__'] = self.fcnNames.get(None,0)
                        del self.fcnNames[None]
                    
                    if self.pa.quietSw:
                        return result
                        
                    hdr = "\nMcCabe Complexity Metric for file %s" % self.inFile
                    print(hdr)
                    print("-"*len(hdr) + "\n")
                    keyList = self.fcnNames.keys()
                    if len( keyList ) > 0:
                        keyList.sort()
                        for k in keyList:
                            if k:
                                name = k
                            else:
                                name = "__main__"
                            print("%11d    %s" % (self.fcnNames[k],name)) 
                            result[k] = self.fcnNames[k]
                    else:
                        print("%11d    %s" % (1,'__main__'))
                        result['__main__'] = 1

                    print
                    return result

            loc = 0
            wordcount = 0
            chrcount = 0
            cmntcount = 0
            classcount = 0
            n1, N1, n2, N2 = 0, 0, 0, 0

            for line in f:
                loc = loc + 1
                chrcount = chrcount + len(line)
                word = line.split(' ')
                wordcount = wordcount + len(word)
                if line.startswith('#'):
                    cmntcount = cmntcount + 1
                if line.startswith('class'):
                    classcount = classcount + 1
            f =open(fPath)
            fd = f.read()
            
            
            stats = os.stat(fPath)
            s = datetime.fromtimestamp(stats.st_atime)
            s1 = datetime.fromtimestamp(stats.st_mtime)
            size1 = stats.st_size
            print("file size in bytes:", size1)
            print('class-count', classcount)
            with open(fPath) as f:
                tree = ast.parse(f.read())
                func = sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)
            '''it's about finding condintion statements and loops'''
            
            i = lizard.analyze_file(fPath)
            analysis = analyze(fd)
            v = ComplexityVisitor.from_code(fd)
            
            hh = h_visit(fd)
            maintainabilityIndex = mi_visit(fd, analysis.multi)
            mirank = mi_rank(maintainabilityIndex)
            mip= mi_parameters(fd, count_multi=True)
            cr = mip[1]
            crank = cc_rank(cr)
            f = open(fPath)
            
            
            lpcountif = lpcountelif = lpcountelse = lpcountfor =lpcountwhile=countwith=countexcept=countfinally=0
            line = f.readlines()
            for x in line:
                if( x == '('):
                    N1 +=1
                if re.search('if ', x):
                    lpcountif = lpcountif + 1
                if re.search('elif ', x):
                    lpcountelif = lpcountelif + 1
                if re.search('else ', x):
                    lpcountelse = lpcountelse + 1
                if re.search('for ', x):
                    lpcountfor = lpcountfor + 1
                if re.search('while ', x):
                    lpcountwhile = lpcountwhile + 1
                if re.search('with ', x):
                    countwith=countwith+1
                if re.search('except:', x):
                    countexcept=countexcept+1
                if re.search('finally:', x):
                    countfinally=countfinally+1

            cmplx=lpcountif+lpcountelif+lpcountelse+lpcountwhile+lpcountfor+1+countexcept+countfinally
            if cmplx<=5 and cmplx>=1:
                perfrmance="Low-simple block"
                rank="A"
            elif cmplx>=6 and cmplx<=10:
                perfrmance="low"
                rank="B"
            elif cmplx>=11 and cmplx<=20:
                perfrmance = "Moderate"
                rank = "C"
            elif cmplx>=21 and cmplx<=30:
                perfrmance = "More than Moderate"
                rank = "D"

            elif cmplx>=31 and cmplx<=40:
                perfrmance = "high"
                rank = "E"
            else:
                perfrmance="very high"
                rank='F'
            message = {"filename": f.name,
                        "lines":analysis[0], 
                        "lloc" : analysis[1],
                        "sloc" : analysis[2],
                        "comments" : analysis[3],
                        "multi" : analysis[4],
                        "blank" : analysis[5],
                        "single_comments" : analysis[5],
                        "linesOfCode" : i.__dict__.get('nloc'),
                        "words": wordcount, "characters": chrcount,
                        "content": fd,
                       "functionscount": func,
                       # "commentlinescount": cmntcount,
                       "cyccom":mip[1],
                       "lastmodifiedtime": s1,
                       "lastaccessedtime": s,
                       "classescount": classcount,
                       "ifloop": lpcountif,
                       "elifloop": lpcountelif,
                       "elseloop": lpcountelse,
                       "filesize":size1,
                       "countexcept":countexcept,
                       "countfinally":countfinally,
                       "forloop": lpcountfor,
                       "whileloop":lpcountwhile,
                       # "cmplx":cmplx,
                       # "rank":rank,
                       # "perf":perfrmance,
                       "cco":i.function_list[0].__dict__,
                       "functionName":i.function_list[0].__dict__.get('name'),
                       "fcc":i.function_list[0].__dict__.get('cyclomatic_complexity'),
                       # "brr": analysis,
                       "v": v.functions[0:],
                       "hh":hh,
                       "h1":hh[0][0],
                       "h2":hh[0][1],
                       "N1":hh[0][2],
                       "N2":hh[0][3],
                       "pv":hh[0][4],
                       "l":hh[0][5],
                       "vo": hh[0][7],
                       "d":hh[0][8],
                       "e":hh[0][9],
                       "t":hh[0][10],
                        "b":hh[0][11],
                       
                       "mi": maintainabilityIndex,
                       "mirank":mirank,
                       "crank":crank,
                       # "mip":mip
                       }
            return render(request, "user/userfiledata1.html", {"message": message})
        except Exception as e:
            print('Exception is ', str(e))
            # messages.success(request, 'Invalid Details')
        return render(request, 'user/userfiledata1.html')

def findfilesloader(request):   
    return render(request, 'user/findfilesloader.html')

def filedata(request):
    if request.method == "GET":
        file = request.GET.get('id')
        try:
            print("file", file)
            head, fileName = os.path.split(file)
            fPath = settings.MEDIA_ROOT + '\\' + 'files\pdfs' + '\\' + fileName
            f = open(fPath)
            class MetricBase( object ):
                """ Metric template class."""
                def __init__( self, *args, **kwds ):
                    pass
                    
                def processSrcLines( self, srcLines, *args, **kwds ):
                    """ Handle physical line after tab expansion."""
                    pass
                    
                def processToken( self, fcnName, className, tok, *args, **kwds ):
                    """ Handle processing after each token processed."""
                    pass
                    
                def processStmt( self, fcnName, className, stmt, *args, **kwds ):
                    """ Handle processing at end of statement."""
                    pass
                    
                def processBlock( self, fcnName, className, block, *args, **kwds ):
                    """ Handle processing at end of block."""
                    pass
                    
                def processFunction( self, fcnName, className, fcn, *args, **kwds ):
                    """ Handle processing at end of function. """
                    pass
                    
                def processClass( self, fcnName, className, cls, *args, **kwds ):
                    """ Handle processing at end of class. """
                    pass
                    
                def processModule( self, moduleName, module, *args, **kwds ):
                    """ Handle processing at end of module. """
                    pass
                    
                def processRun( self, run, *args, **kwds ):
                    """ Handle processing at end of run. """
                    pass

                def compute( self, *args, **kwds ):
                    """ Compute the metric given all needed info known."""
                    pass
                    
            class HalsteadMetric( MetricBase ):
                """ Compute various HalsteadMetric metrics. """
                totalV = 0
                totalE = 0
                numModules = 0
                def __init__( self, context, runMetrics, metrics, pa, *args, **kwds ):
                    """ Initialization for the HalsteadMetric metrics."""
                    self.inFile = context['inFile']
                    self.context = context
                    self.runMetrics = runMetrics
                    self.metrics = metrics
                    self.pa = pa
                    self.inFile = context['inFile']
                    self.numOperators = 0
                    self.numOperands = 0
                    self.uniqueOperators = {}
                    self.uniqueOperands = {}
                    HalsteadMetric.numModules += 1
                    
                    # initialize category accummulators as dictionaries
                    self.hsDict = {}
                    for t in ['token','stmt','block','function','class','module','run']:
                        self.uniqueOperators[t] = {}
                        self.uniqueOperands[t] = {}
                        #for v in ['N','N1','N2','n','n1','n2','V','D','E','avgV','avgE']:
                        #    self.hsDict[(t,v)] = 0
                    
                def processToken( self, currentFcn, currentClass, tok, *args, **kwds ):
                    """ Collect token data for Halstead metrics."""
                    if tok.type in [WS, EMPTY, ENDMARKER, NEWLINE, EMPTY, COMMENT]:
                        pass
                    elif tok.type in [OP, INDENT, DEDENT]:
                        self.numOperators += 1
                        self.uniqueOperators['token'][tok.text] = self.uniqueOperators['token'].get(tok.text, 0) + 1
                    else:
                        self.numOperands += 1
                        sDict = self.context.__repr__()
                        k = (sDict,tok.text)
                        self.uniqueOperands['token'][k] = self.uniqueOperands['token'].get(tok.text, 0) + 1

                def processStmt( self, currentFcn, currentClass, stmt, *args, **kwds ):
                    """ Collect statement data for Halstead metrics."""
                    
                    result = None
                    
                    # the two lines following this comment would compute the Halstead 
                    # metrics for each statement in the run, However, it is 
                    # normally overkill, so these lines are commented out.
                    
                    #lineNum = stmt[0].row
                    #result = self.computeCategory( 'stmt', lineNum, stmt )
                    
                    return result
                    
                def processBlock( self, currentFcn, currentClass, block, *args, **kwds ):
                    """ Collect block data for Halstead metrics."""

                    result = None

                    # the two lines following this comment would compute the Halstead 
                    # metrics for each statement in the run, However, it is 
                    # normally overkill, so the two lines are commented out.
                    
                    #blockNum = self.context['blockNum']
                    #result = self.computeCategory( 'block', blockNum, block )
                    
                    return result

                def processFunction( self, currentFcn, currentClass, fcn, *args, **kwds ):
                    """ Collect function data for Halstead metrics."""
                    result = self.computeCategory( 'function', currentFcn, fcn )
                    return result
                    
                def processClass( self, currentFcn, currentClass, cls, *args, **kwds ):
                    """ Collect class data for Halstead metrics."""
                    result = self.computeCategory( 'class', currentClass, cls )
                    return result
                    
                def processModule( self, moduleName, mod, *args, **kwds ):
                    """ Collect module data for Halstead metrics."""
                    result = self.computeCategory( 'module', moduleName, mod )
                    return result
                    
                def processRun( self, run, *args, **kwds ):
                    """ Collect run data for Halstead metrics."""
                    datestamp = time.strftime("%Y-%m-%d.%H:%m%Z",time.localtime())
                    result = self.computeCategory( 'run', datestamp, run )
                    return result
                    
                def __LOGb( self, x, b ): 
                    """ convert to LOGb(x) from natural logs."""
                    try:
                        result = math.log( x ) / math.log ( b )
                    except OverflowError:
                        result = 1.0
                    return result

                def computeIncr( self, cat, tok, uniqueOperators, uniqueOperands ):
                    """ Compute increment for token depending on which category it falls into."""
                    operatorIncr = operandIncr = 0
                    if tok.type in [WS, EMPTY, ENDMARKER, NEWLINE, EMPTY, COMMENT]:
                        return (operatorIncr,operandIncr)
                        
                    if tok.type in [OP, INDENT, DEDENT]:
                        operatorIncr = 1
                        uniqueOperators[tok.text] = uniqueOperators.get(tok.text, 0) + 1
                    else:
                        operandIncr = 1
                        uniqueOperands[tok.text] = uniqueOperands.get(tok.text,0) + 1
                        
                    return (operatorIncr,operandIncr)
                    
                def computeCategory( self, cat, mod, lst ):
                    """ Collection data for cat of code."""
                    modID= id( mod )
                    numOperators = numOperands = 0
                    for tok in lst:
                        result = self.computeIncr( cat, tok, self.uniqueOperators[cat], self.uniqueOperands[cat] )
                        numOperators += result[0]
                        numOperands += result[1]
                    result = self.compute( cat, modID, numOperators, numOperands, self.uniqueOperators[cat], self.uniqueOperands[cat] )
                    return result
                    
                def compute( self, cat, modID, numOperators, numOperands, uniqueOperators, uniqueOperands, *args, **kwds ):
                    """ Do actual calculations here."""
                    
                    n1 = len( uniqueOperands )
                    n2 = len( uniqueOperators )
                    N1 = numOperands
                    N2 = numOperators
                    N = N1 + N2
                    n = n1 + n2
                    V = float(N) * self.__LOGb( n, 2 )
                    try:
                        D = (float(n1)/2.0) * (float(N2)/float(n2))
                    except ZeroDivisionError:
                        D = 0.0
                    E = D * V
                    HalsteadMetric.totalV += V
                    HalsteadMetric.totalE += E
                    avgV = HalsteadMetric.totalV / HalsteadMetric.numModules
                    avgE = HalsteadMetric.totalE / HalsteadMetric.numModules
                    
                    self.hsDict[(cat,modID,'n1')] = n1
                    self.hsDict[(cat,modID,'n2')] = n2
                    self.hsDict[(cat,modID,'N1')] = N1
                    self.hsDict[(cat,modID,'N2')] = N2
                    self.hsDict[(cat,modID,'N')] = N
                    self.hsDict[(cat,modID,'n')] = n
                    self.hsDict[(cat,modID,'V')] = V
                    self.hsDict[(cat,modID,'D')] = D
                    self.hsDict[(cat,modID,'E')] = E
                    self.hsDict[(cat,modID,'numModules')] = HalsteadMetric.numModules
                    self.hsDict[(cat,modID,'avgV')] = avgV
                    self.hsDict[(cat,modID,'avgE')] = avgE
                    
                    return self.hsDict
                    
                def display( self, cat=None ):
                    """ Display the computed Halstead Metrics."""
                    if self.pa.quietSw:
                        return self.hsDict
                        
                    hdr = "\nHalstead Metrics for %s" % self.inFile
                    print(hdr)
                    print("-"*len(hdr) + '\n')
                    
                    if len( self.hsDict ) == 0:
                        print ("%-8s %-30s " % ('**N/A**','All Halstead metrics are zero'))
                        return self.hsDict
                        
                    keyList = self.hsDict.keys()
                    keyList.sort()
                    if 0:
                        for k,i,v in keyList:
                            if cat:
                                if k!=cat:
                                    continue
                            print("%14.2f %s %s %s" % (self.hsDict[(k,i,v)],k,i,v) )
                        print( hdr1 = "Category Identifier                                D        E     N   N1   N2        V     avgE     avgV     n   n1   n2",
                    hdr2 = "-------- ---------------------------------- -------- -------- ----- ---- ---- -------- -------- -------- ----- ---- ----")
                    #       12345678 123456789012345678901234567890  12345678 12345678 12345 1234 1234 12345678 12345678 12345678 12345 1234 1234
                    fmt1 = "%-8s %-33s "
                    fmt2 = "%8.2e %8.2e %5d %4d %4d %8.2e %8.2e %8.2e %5d %4d %4d"
                    
                    # this loop uses the Main Line Standards break logic. It does this to convert the
                    # normal vertical output to a horizontal format. The control variables are the
                    # category name and the identifier value.
                    
                    oldK = oldI = None
                    vDict = {}
                    vList = []
                    hdrSw = True                # output header for first time thru
                    for k,i,v in keyList:
                        # only print data for the category we want
                        if cat:
                            if k != cat:
                                continue 
                                
                        if v == "numModules":    # ignore this value for now
                            continue
                            
                        if (oldK,oldI) != (k,i):    # change in category/id
                            if oldK and oldI:           # this is not first time thru
                                #t = tuple([self.hsDict[(k,i,v)] for v in vList])
                                t = tuple([vDict[v] for v in vList])
                                print(fmt1 % (k,i))
                                print (fmt2 % t)
                            # initialize for next set of category/id
                            vDict = {}
                            vDict[v] = self.hsDict[(k,i,v)]
                            vList = []
                            vList.append( v )
                            oldK = k
                            oldI = i
                            if hdrSw:
                                print(hdr1)
                                print(hdr2)
                                hdrSw = False
                        else:       # we are still in the same category/id
                            vDict[v] = self.hsDict[(k,i,v)]
                            vList.append( v )

                    print
                            
                    return self.hsDict
                McCabeKeywords = {
                'assert':0,
                'break':1,
                'continue':1,
                'elif':1,
                'else':1,
                'for':1,
                'if':1,
                'while':1
                }
                
            class McCabeMetric( MetricBase ):
                """ Compute McCabe's Cyclomatic McCabeMetric by function."""
                def __init__( self, context, runMetrics, metrics, pa, *args, **kwds ):
                    self.context = context
                    self.runMetrics = runMetrics
                    self.metrics = metrics
                    self.pa = pa
                    self.inFile = context['inFile']
                    self.fcnNames = {}
                            
                def processToken( self, fcnName, className, tok, *args, **kwds ):
                    """ Increment number of decision points in function."""
                    if tok and tok.text in McCabeKeywords:
                        self.fcnNames[fcnName] = self.fcnNames.get(fcnName,0) + 1
                
                def processFunction( self, fcnName, className, fcn, *args, **kwds ):
                    """ Increment number of decision points in function."""
                    self.fcnNames[fcnName] = self.fcnNames.get(fcnName,0) + 1
                
                def display( self ):
                    """ Display McCabe Cyclomatic metric for each function """
                    result = {}
                    # the next three lines ensure that fcnNames[None] is treated
                    # like fcnNames['__main__'] and are sorted into alphabetical
                    # order.
                    if self.fcnNames.has_key(None):
                        self.fcnNames['__main__'] = self.fcnNames.get(None,0)
                        del self.fcnNames[None]
                    
                    if self.pa.quietSw:
                        return result
                        
                    hdr = "\nMcCabe Complexity Metric for file %s" % self.inFile
                    print(hdr)
                    print("-"*len(hdr) + "\n")
                    keyList = self.fcnNames.keys()
                    if len( keyList ) > 0:
                        keyList.sort()
                        for k in keyList:
                            if k:
                                name = k
                            else:
                                name = "__main__"
                            print("%11d    %s" % (self.fcnNames[k],name)) 
                            result[k] = self.fcnNames[k]
                    else:
                        print("%11d    %s" % (1,'__main__'))
                        result['__main__'] = 1

                    print
                    return result

            loc = 0
            wordcount = 0
            chrcount = 0
            cmntcount = 0
            classcount = 0
            n1, N1, n2, N2 = 0, 0, 0, 0

            for line in f:
                loc = loc + 1
                chrcount = chrcount + len(line)
                word = line.split(' ')
                wordcount = wordcount + len(word)
                if line.startswith('#'):
                    cmntcount = cmntcount + 1
                if line.startswith('class'):
                    classcount = classcount + 1
            f =open(fPath)
            fd = f.read()
            
            
            stats = os.stat(fPath)
            s = datetime.fromtimestamp(stats.st_atime)
            s1 = datetime.fromtimestamp(stats.st_mtime)
            size1 = stats.st_size
            print("file size in bytes:", size1)
            print('class-count', classcount)
            with open(fPath) as f:
                tree = ast.parse(f.read())
                func = sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)
            '''it's about finding condintion statements and loops'''
            
            i = lizard.analyze_file(fPath)
            analysis = analyze(fd)
            v = ComplexityVisitor.from_code(fd)
            
            hh = h_visit(fd)
            maintainabilityIndex = mi_visit(fd, analysis.multi)
            mirank = mi_rank(maintainabilityIndex)
            mip= mi_parameters(fd, count_multi=True)
            cr = mip[1]
            crank = cc_rank(cr)
            f = open(fPath)
            
            
            lpcountif = lpcountelif = lpcountelse = lpcountfor =lpcountwhile=countwith=countexcept=countfinally=0
            line = f.readlines()
            for x in line:
                if( x == '('):
                    N1 +=1
                if re.search('if ', x):
                    lpcountif = lpcountif + 1
                if re.search('elif ', x):
                    lpcountelif = lpcountelif + 1
                if re.search('else ', x):
                    lpcountelse = lpcountelse + 1
                if re.search('for ', x):
                    lpcountfor = lpcountfor + 1
                if re.search('while ', x):
                    lpcountwhile = lpcountwhile + 1
                if re.search('with ', x):
                    countwith=countwith+1
                if re.search('except:', x):
                    countexcept=countexcept+1
                if re.search('finally:', x):
                    countfinally=countfinally+1

            cmplx=lpcountif+lpcountelif+lpcountelse+lpcountwhile+lpcountfor+1+countexcept+countfinally
            if cmplx<=5 and cmplx>=1:
                perfrmance="Low-simple block"
                rank="A"
            elif cmplx>=6 and cmplx<=10:
                perfrmance="low"
                rank="B"
            elif cmplx>=11 and cmplx<=20:
                perfrmance = "Moderate"
                rank = "C"
            elif cmplx>=21 and cmplx<=30:
                perfrmance = "More than Moderate"
                rank = "D"

            elif cmplx>=31 and cmplx<=40:
                perfrmance = "high"
                rank = "E"
            else:
                perfrmance="very high"
                rank='F'
            message = {"filename": f.name,
                        "lines":analysis[0], 
                        "lloc" : analysis[1],
                        "sloc" : analysis[2],
                        "comments" : analysis[3],
                        "multi" : analysis[4],
                        "blank" : analysis[5],
                        "single_comments" : analysis[5],
                        "linesOfCode" : i.__dict__.get('nloc'),
                        "words": wordcount, "characters": chrcount,
                        "content": fd,
                       "functionscount": func,
                       # "commentlinescount": cmntcount,
                       "cyccom":mip[1],
                       "lastmodifiedtime": s1,
                       "lastaccessedtime": s,
                       "classescount": classcount,
                       "ifloop": lpcountif,
                       "elifloop": lpcountelif,
                       "elseloop": lpcountelse,
                       "filesize":size1,
                       "countexcept":countexcept,
                       "countfinally":countfinally,
                       "forloop": lpcountfor,
                       "whileloop":lpcountwhile,
                       # "cmplx":cmplx,
                       # "rank":rank,
                       # "perf":perfrmance,
                       "cco":i.function_list[0].__dict__,
                       "functionName":i.function_list[0].__dict__.get('name'),
                       "fcc":i.function_list[0].__dict__.get('cyclomatic_complexity'),
                       # "brr": analysis,
                       "v": v.functions[0:],
                       "hh":hh,
                       "h1":hh[0][0],
                       "h2":hh[0][1],
                       "N1":hh[0][2],
                       "N2":hh[0][3],
                       "pv":hh[0][4],
                       "l":hh[0][5],
                       "vo": hh[0][7],
                       "d":hh[0][8],
                       "e":hh[0][9],
                       "t":hh[0][10],
                        "b":hh[0][11],
                       
                       "mi": maintainabilityIndex,
                       "mirank":mirank,
                       "crank":crank,
                       # "mip":mip
                       }
            return render(request, "admin/filedata.html", {"message": message})
        except Exception as e:
            print('Exception is ', str(e))
            # messages.success(request, 'Invalid Details')
        return render(request, 'admin/filedata.html')




def que1(request):
    return render(request, "user/Problems/que1.html")
def que2(request):
    return render(request, "user/Problems/que2.html")
def que3(request):
    return render(request, "user/Problems/que3.html")
def que4(request):
    return render(request, "user/Problems/que4.html")
def que5(request):
    return render(request, "user/Problems/que5.html")
def que6(request):
    return render(request, "user/Problems/que6.html")
def que7(request):
    return render(request, "user/Problems/que7.html")
def que8(request):
    return render(request, "user/Problems/que8.html")
def que9(request):
    return render(request, "user/Problems/que9.html")
def que10(request):
    return render(request, "user/Problems/que10.html")

def que11(request):
    return render(request, "user/Problems/que11.html")
def que12(request):
    return render(request, "user/Problems/que12.html")
def que13(request):
    return render(request, "user/Problems/que13.html")
def que14(request):
    return render(request, "user/Problems/que14.html")
def que15(request):
    return render(request, "user/Problems/que15.html")
def que16(request):
    return render(request, "user/Problems/que16.html")
def que17(request):
    return render(request, "user/Problems/que17.html")
def que18(request):
    return render(request, "user/Problems/que18.html")
def que19(request):
    return render(request, "user/Problems/que19.html")
def que20(request):
    return render(request, "user/Problems/que20.html")
def que21(request):
    return render(request, "user/Problems/que21.html")
def que22(request):
    return render(request, "user/Problems/que22.html")
def que23(request):
    return render(request, "user/Problems/que23.html")
def que24(request):
    return render(request, "user/Problems/que24.html")
def que25(request):
    return render(request, "user/Problems/que25.html")
def que26(request):
    return render(request, "user/Problems/que26.html")
def que27(request):
    return render(request, "user/Problems/que27.html")
def que28(request):
    return render(request, "user/Problems/que28.html")
def que29(request):
    return render(request, "user/Problems/que29.html")
def que30(request):
    return render(request, "user/Problems/que30.html")
def que31(request):
    return render(request, "user/Problems/que31.html")
def que32(request):
    return render(request, "user/Problems/que32.html")
def que33(request):
    return render(request, "user/Problems/que33.html")
def que34(request):
    return render(request, "user/Problems/que34.html")
def que35(request):
    return render(request, "user/Problems/que35.html")

def que36(request):
    return render(request, "user/Problems/que36.html")
def que37(request):
    return render(request, "user/Problems/que37.html")
def que38(request):
    return render(request, "user/Problems/que38.html")
def que39(request):
    return render(request, "user/Problems/que39.html")
def que40(request):
    return render(request, "user/Problems/que40.html")
def que41(request):
    return render(request, "user/Problems/que41.html")
def que42(request):
    return render(request, "user/Problems/que42.html")
def que43(request):
    return render(request, "user/Problems/que43.html")
def que44(request):
    return render(request, "user/Problems/que44.html")
def que45(request):
    return render(request, "user/Problems/que45.html")
def que46(request):
    return render(request, "user/Problems/que46.html")
def que47(request):
    return render(request, "user/Problems/que47.html")
def que48(request):
    return render(request, "user/Problems/que48.html")
def que49(request):
    return render(request, "user/Problems/que49.html")
def que50(request):
    return render(request, "user/Problems/que50.html")











#
# def que1(request):
#     return render(request, "user/que1.html")

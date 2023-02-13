// "Search"
// This macro searches for text in files contained in a directory.
// TF, 2011.02 Added support for scripts; Recordable.


// variables for memory release

var collectGarbageInterval = 10; // the garbage is collected after n Images
var collectGarbageCurrentIndex = 1; // increment variable for garbage collection
var collectGarbageWaitingTime = 100; // waiting time in milliseconds before garbage is collected
var collectGarbageRepetitionAttempts = 1; // repeats the garbage collection n times
var collectGarbageShowLogMessage = true; // defines whether or not a log entry will be made

//


  str = "";
  contents = true;
  ignore = false;
  cxa = false;
  putlabels = false;
  firstLine = true;
  arg = getArgument;
  if (arg!="") {
      args = split(arg, "|");
      if (args.length==5) {
          str = args[0];
          contents = parseInt(args[1]);
          ignore = parseInt(args[2]);
          ignore = parseInt(args[3]);
          putlabels = parseInt(args[4]);
       }
  }
  extensions = newArray(".java", ".txt", ".ijm", ".js", ".py", ".rb", ".clj", ".bsh", ".html");
  IJdir = getDirectory("imagej");

  Dialog.create("Looking for images");
  Dialog.addString("_", ".tif", 20);
  Dialog.setInsets(2,20,0);
  Dialog.addCheckbox("Search_contents", contents);
  Dialog.addCheckbox("Ignore case", ignore);
  Dialog.addCheckbox("Data from cx-a ?", cxa);
  Dialog.addCheckbox("add labels ?", putlabels);
  Dialog.setInsets(10, 0, 0);
  Dialog.addMessage("Press OK and select the folder containing your exported 3D tiffs");
  
  Dialog.show();
  str = Dialog.getString();
  contents = Dialog.getCheckbox();
  ignore = Dialog.getCheckbox();
  cxa = Dialog.getCheckbox();
  putlabels = Dialog.getCheckbox();
  
  if (str=="")
     exit("Search string is empty");

  sourceExists = File.exists(IJdir+"source");
  searchNames = false;
  dir1=""; 
  dir1 = getDirectory("Choose a Directory");
  searchNames = true;
  if (ignore)
      str = toLowerCase(str);
  count = 0;
  if (dir1!="") find(dir1);
  if (indexOf(str, "|")==-1)
      return ""+str+"|"+contents+"|"+ignore;
  exit; 

  function find(dir) {
      list = getFileList(dir);
      for (i=0; i<list.length; i++) {
          showProgress(i, list.length);
          if (endsWith(list[i], "/"))
              find(""+dir+list[i]);
          else if (contents && valid(list[i])) {
              s = File.openAsString(dir+list[i]);
              s2 = s;
              if (ignore)
                  s2 = toLowerCase(s);
              if (indexOf(s2,str)!=-1) {
                  count++;
                  if (firstLine)
                      showMessageInHeader();
                  print("");
                  print(dir+list[i]);
                  lines = split(s, "\n");
                  n = 0;

                  for (j=0; j<lines.length; j++) {
                      line = lines[j];
                      line2 = line;
                      if (ignore) line2 = toLowerCase(line);
                      if (indexOf(line2,str)!=-1 && n<8) {
                          print((j+1)+": "+line);
                          n++;
                      }
                 } // for
              } else
                  searchName(list[i],cxa);
          } else if (searchNames || valid(list[i]))
              searchName(list[i],cxa);
      }
      if (count==1)
          showStatus("1 match");
      else
          showStatus(count+" matches");

          //END of the loop insert  here last macro(s) 
setBatchMode(false);
run("Image Sequence...", "open=["+dir+"/MAXproj/] sort");
run("Brightness/Contrast...");
 
waitForUser("ADJUST CONTRAST");

  
  Dialog.create("Time setting");
  Dialog.addNumber("how many frames ? :",0 );
  Dialog.addNumber("final size ? :",1080 );
  Dialog.addNumber("Give me the time interval in seconds:",0 );
 // Dialog.addString("sec, min, hrs ?","" );
  Dialog.addNumber("Movie Frame Rate:",3 );
  Dialog.addString("Movie Title","" );
  Dialog.show();
  z = Dialog.getNumber();
  xy = Dialog.getNumber();
  k = Dialog.getNumber();     
  l = Dialog.getNumber();
  m = Dialog.getString(); 
 //m = Dialog.getString();



run("RGB Color");

if(!putlabels){
if (!cxa){
makeRectangle(1, 1, 472, 472);
}
run("Size...", "width="+xy+" height="+xy+" depth="+z+" constrain average interpolation=Bilinear");
run("AVI... ", "compression=None frame="+l+" save=["+dir+"/MAXproj_Movie/MAXproj_"+m+".avi"]); 
saveAs("Tiff", dir+"/MAXproj_Movie/MAXproj_"+m+".tiff");
}

if(putlabels){
	
run("Set Scale...", "distance=512 known=90 pixel=1 unit=um global");
makeRectangle(34, 22, 92, 13);
run("Scale Bar...", "width=10 height=5 font=15 color=White background=None location=[At Selection] bold label");
run("RGB Color");
//run("Time Stamper", "digital=1 starting=0 interval="+k+" x=34 y=70 font=17 decimal=0 anti-aliased or="+j);
run("Label...", "format=00:00:00 x=34 y=70 font=17 text=h:m:s starting=0 interval="+k+"");

if (!cxa){
run("Label...", "format=Text x=34 y=458 font=17 text="+m+"");
}
if (cxa){
run("Label...", "format=Text x=34 y=434 font=17 text="+m+"");
}


if (!cxa){
makeRectangle(1, 1, 472, 472);
}
if (cxa){
makeRectangle(1, 1, 448, 448);
}
run("Size...", "width="+xy+" height="+xy+" depth="+z+" constrain average interpolation=Bilinear");
run("AVI... ", "compression=None frame="+l+" save="+dir+"/MAXproj_Movie/MAXproj_"+m+".avi");
saveAs("Tiff", dir+"/MAXproj_Movie/MAXproj_"+m+".tiff");
}




  }

  function searchName(name,cxa) {
      name2 = name;
      if (ignore)
          name2 = toLowerCase(name2);
      if (indexOf(name2,str)!=-1) {
          if (firstLine)
              showMessageInHeader();
       
        File.makeDirectory(dir+"MAXproj");
         File.makeDirectory(dir+"MAXproj_Movie");
//  insert macro here to modify the files of interest



 setBatchMode(true);
run("Bio-Formats Importer", "open=["+dir+name+"] color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT use_virtual_stack");

 resetMinAndMax();

 if (nSlices==1) {
 	if (!cxa){
 	makeRectangle(22, 22, 472, 472);
 	run("Crop");
 	}	
saveAs("Tiff", dir+"/MAXproj/Max_"+name);
 } 
else  {
run("Z Project...", "projection=[Max Intensity]"); //start=5 stop=10
 	
if (!cxa){
 	makeRectangle(22, 22, 472, 472);
 	run("Crop");
 	}	

saveAs("Tiff", dir+"/MAXproj/Max_"+name);
} 


close("*");
 
 } 
          count++;
   

//-------------------------------------------------------------------------------------------
// this function collects garbage after a certain interval
//-------------------------------------------------------------------------------------------
function collectGarbageIfNecessary(){
if(collectGarbageCurrentIndex == collectGarbageInterval){
setBatchMode(false);
wait(collectGarbageWaitingTime);
for(i=0; i<collectGarbageRepetitionAttempts; i++){
wait(100);
run("Collect Garbage");
call("java.lang.System.gc");
}
if(collectGarbageShowLogMessage) print("...Collecting Garbage...");
collectGarbageCurrentIndex = 1;
setBatchMode(true);
}
else collectGarbageCurrentIndex++;
}
      }

  }

  function valid(name) {
      for (i=0; i<extensions.length; i++) {
         if (endsWith(name, extensions[i]))
             return true;
      }
      return false;
  }
  
  function showMessageInHeader() {
      print("\\Heading: Double-click on a file name to open it");
      firstLine = false;


}

 
               

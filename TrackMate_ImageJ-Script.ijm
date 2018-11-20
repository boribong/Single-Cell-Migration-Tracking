sourceDir = getDirectory("Choose Source Directory ");
targetDir = getDirectory("Choose Destination Directory ");
list = getFileList(sourceDir);
setBatchMode(true);
for (i=0; i<list.length; i++) {
	open(sourceDir+list[i]);
	name = File.nameWithoutExtension;
	script = File.openAsString("TrackMate_Python-Script.py"); 
	eval("python", script);
	var spotsTabName="Spots in tracks statistics";
	var linksTabName="Links in tracks statistics";
	var tracksTabName="Track statistics";
	selectWindow(spotsTabName);
	saveAs("Text", targetDir+name+"_spots.csv");
	run("Close");
	selectWindow(linksTabName);
	saveAs("Text", targetDir+name+"_links.csv");
	run("Close");
	selectWindow(tracksTabName);
	saveAs("Text", targetDir+name+"_tracks.csv");
	run("Close");
	close();
}
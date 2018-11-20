from fiji.plugin.trackmate import Model
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate.detection import DownsampleLogDetectorFactory
from fiji.plugin.trackmate.tracking.oldlap import LAPTrackerFactory
from fiji.plugin.trackmate.detection import DetectorKeys
from fiji.plugin.trackmate.tracking import LAPUtils
from fiji.plugin.trackmate.action import ExportStatsToIJAction
from fiji.plugin.trackmate.action import TrackBranchAnalysis
from fiji.plugin.trackmate.graph import GraphUtils
from ij.plugin import HyperStackConverter
from ij.measure import ResultsTable
from ij import IJ
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
import fiji.plugin.trackmate.features.track.TrackDurationAnalyzer as TrackDurationAnalyzer
  
import sys
from java.io import File
from fiji.plugin.trackmate.io import TmXmlWriter

imp = IJ.getImage()

impconv = HyperStackConverter()
imp = impconv.toHyperStack(imp, 1, 1, imp.getStackSize())

imp.show()

#----------------------------
# Create the model object now
#----------------------------

model = Model()

# Send all messages to ImageJ log window.
model.setLogger(Logger.IJ_LOGGER)

#------------------------
# Prepare settings object
#------------------------
   
settings = Settings()
settings.setFrom(imp)
   
# Configure detector - We use the Strings for the keys
settings.detectorFactory = DownsampleLogDetectorFactory()
settings.detectorSettings = {
	DetectorKeys.KEY_RADIUS: 5.,
	DetectorKeys.KEY_DOWNSAMPLE_FACTOR: 4,
	DetectorKeys.KEY_THRESHOLD : 1.,
}
print(settings.detectorSettings)

# Config initial spot filters value
settings.initialSpotFilterValue = 3.5

# Configure spot filters - Classical filter on quality
#filter1 = FeatureFilter('QUALITY', 2.3, True)
#settings.addSpotFilter(filter1)

# Configure tracker - We want to allow merges and fusions
settings.trackerFactory = LAPTrackerFactory()
settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap() # almost good enough
print(LAPUtils.getDefaultLAPSettingsMap())
settings.trackerSettings['LINKING_MAX_DISTANCE'] = 50 #15.0
settings.trackerSettings['LINKING_FEATURE_PENALTIES'] = {}
#gap closing
settings.trackerSettings['ALLOW_GAP_CLOSING'] = True
settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE'] = 50.0 #15.0
settings.trackerSettings['MAX_FRAME_GAP'] = 2 #5
settings.trackerSettings['GAP_CLOSING_FEATURE_PENALTIES'] = {}
#splitting
settings.trackerSettings['ALLOW_TRACK_SPLITTING'] = False
settings.trackerSettings['SPLITTING_MAX_DISTANCE'] = 15.0
settings.trackerSettings['SPLITTING_FEATURE_PENALTIES'] = {}
#merging
settings.trackerSettings['ALLOW_TRACK_MERGING'] = False
settings.trackerSettings['MERGING_MAX_DISTANCE'] = 15.0
settings.trackerSettings['MERGING_FEATURE_PENALTIES'] = {}
#etc
#settings.trackerSettings['ALTERNATIVE_LINKING_COST_FACTOR'] = 1.05
#settings.trackerSettings['BLOCKING_VALUE'] = Infinity
#settings.trackerSettings['CUTOFF_PERCENTILE'] = 0.9			

# Configure track analyzers
# The displacement feature is provided by the TrackDurationAnalyzer.

settings.addTrackAnalyzer(TrackDurationAnalyzer())

# Configure track filters - We want to get rid of the two immobile spots

filter2 = FeatureFilter('TRACK_DISPLACEMENT', 10, True)
settings.addTrackFilter(filter2)

#-------------------
# Instantiate plugin
#-------------------

trackmate = TrackMate(model, settings)
   
#--------
# Process
#--------

ok = trackmate.checkInput()
if not ok:
	sys.exit(str(trackmate.getErrorMessage()))

ok = trackmate.process()
if not ok:
	sys.exit(str(trackmate.getErrorMessage()))

#----------------
# Display results
#----------------
 
selectionModel = SelectionModel(model)
displayer =  HyperStackDisplayer(model, selectionModel, imp)
displayer.render()
displayer.refresh()

# Echo results with the logger we set at start:
model.getLogger().log(str(model))

# export needed files for further analysis

#outfile = TmXmlWriter(File('/home/boribong/Desktop/'))
#outfile.appendModel(model)
#outfile.writeToFile()

# show dialog windows
## THIS HAS TO BE AUTOMATED

esta = ExportStatsToIJAction()
results = esta.execute(trackmate)

print(type(results))

#tba = TrackBranchAnalysis(selectionModel)
#tba.execute(trackmate)

# echo feature model

#print(trackmate.getModel().getTrackModel().echo())

###############################################
##Dmitry Sutormin, 2019##
##ChIP-Seq analysis##

####
#The only purpose - to compute by-position average of a set of wig files.
####

###############################################

#######
#Packages to be imported.
#######

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm as cm

#Dictionary of replicas 
#'Replica name' : 'Path to wig file'
Dict_of_replicas={'Replic 1' : "F:\Gyrase_time-course_experiment\Reads_eq\WIG_files\Fold_enrichment\Gyrase_tc_Topo-Seq_20min_1_FE.wig",
                  'Replic 2' : "F:\Gyrase_time-course_experiment\Reads_eq\WIG_files\Fold_enrichment\Gyrase_tc_Topo-Seq_20min_2_FE.wig",
                  }

#ID or short description of the track (will be the name of a track in IGV).
name='Gyrase_tc_Topo-Seq_20min_FE'
#ID of chromosome (for w3110_Mu_SGS: NC_007779.1_w3110_Mu)
Chromosome_name='NC_007779.1_w3110_Mu'
#Output path for the final file.
average_file_path="F:\Gyrase_time-course_experiment\Reads_eq\WIG_files\Fold_enrichment\Gyrase_tc_Topo-Seq_20min_average_FE_Early_Stat.wig"
#Output path for the corralation matrix.
Outpath="F:\Gyrase_time-course_experiment\Reads_eq\WIG_files\Fold_enrichment\Gyrase_tc_Topo-Seq_20min_FE_correlation_matrix.png"


#######
#Parses WIG file.
#######

def wig_parsing(wigfile):
    print('Now is processing: ' + str(wigfile))
    wigin=open(wigfile, 'r')
    NE_values=[]
    for line in wigin:
        line=line.rstrip().split(' ')
        if line[0] not in ['track', 'fixedStep']:
            NE_values.append(float(line[0]))
    wigin.close()
    return NE_values

#Contains data of all replicas in separate arrays.
dict_of_replicas={}
for replica_name, replica_path in Dict_of_replicas.items():
    dict_of_replicas[replica_name]=wig_parsing(replica_path)

#########
##Compute correlation matrix and draw heatmaps.
#########

#Plot diagonal correlation matrix.
def correlation_matrix(df, cor_method, title, outpath):
    fig=plt.figure(figsize=(8,8), dpi=100)
    ax1=fig.add_subplot(111)
    cmap=cm.get_cmap('rainbow', 30)
    cax=ax1.imshow(df.corr(method=cor_method), interpolation="nearest", cmap=cmap, norm=None, vmin=-1, vmax=1)
    ax1.grid(True, which='minor', linestyle="--", linewidth=0.5, color="black")
    plt.title(title)
    labels=list(df)
    ax1.set_xticks(np.arange(len(labels)))
    ax1.set_yticks(np.arange(len(labels)))    
    ax1.set_xticklabels(labels, fontsize=12, rotation=90)
    ax1.set_yticklabels(labels, fontsize=12)
    #Add colorbar, make sure to specify tick locations to match desired ticklabels.
    #Full scale:[-1.00, -0.95, -0.90, -0.85, -0.80, -0.75, -0.70, -0.65, -0.60, -0.55, -0.50, -0.45, -0.40, -0.35, -0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00])
    fig.colorbar(cax, ticks=[-1.00, -0.90, -0.80, -0.70, -0.60, -0.50, -0.40, -0.30, -0.20, -0.10, 0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00], shrink=0.7)
    plt.tight_layout()
    plt.savefig(outpath, dpi=400, figsize=(8, 8))
    plt.show()
    plt.close()
    return

correlation_matrix(pd.DataFrame(dict_of_replicas), 'pearson', 'Correlation of biological replicas', Outpath)


#Write file with avaraged data.
average_out=open(average_file_path, 'w')
average_out.write('track type=wiggle_0 name="'+name+'" autoScale=off viewLimits=0.0:25.0\nfixedStep chrom='+Chromosome_name+' start=1 step=1\n')

for i in range(len(dict_of_replicas[list(dict_of_replicas.keys())[0]])):
    av_data_position=[]
    for replica_name, replica_data in dict_of_replicas.items():
        av_data_position.append(replica_data[i])
    average_out.write(str(np.mean(av_data_position))+'\n')

average_out.close()
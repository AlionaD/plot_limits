import re
import matplotlib.pyplot as plt


def extract_unique_substrings_from_list(input_list):

    pattern = r'#(.*?)#.*?#(.*?)(Up|Down);'
    input_string = ' '.join(input_list)
    matches = re.findall(pattern, input_string)
    unique_match_0 = set(match[0] for match in matches)
    unique_match_1 = set(match[1] for match in matches)
    
    unique_match_1 = [i for i in unique_match_1 if '#' not in i]
    unique_match_0.remove('data_obs')
    
    return list(unique_match_0), list(unique_match_1)

def print_nus(nominal, up, down, nominal_ratio, 
              up_ratio, down_ratio, name, filename=None, 
              Xaxis= 'X-axis', MC= "Sum of all MC samples", 
              region = "ee signal low"):
                
    fig, (ax_main, ax_ratio) = plt.subplots(2, 1, figsize=(6, 6), sharex=True, gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

    ax_main.text(0., 1., "CMS Simulation",
        fontsize=14,
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax_main.transAxes,
        fontweight='bold'
        )
    ax_main.text(0.55, 1., "$Work$ $in$ $Progress$",
        fontsize=14,
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax_main.transAxes,
        #fontweight='bold'
        )
    
    ax_main.errorbar(down[0], down[1], yerr=down[2], xerr=down[3], fmt='.', color='#1446A0', label='Down')
    ax_main.errorbar(up[0], up[1], yerr=up[2], xerr=up[3], fmt='.', color='#B40424', label="Up")
    ax_main.errorbar(nominal[0], nominal[1], yerr=nominal[2], xerr=nominal[3], fmt='.', color='black', label="Nominal")

    ax_main.set_ylabel(r"nEntries (Normalized)")
    ax_main.set_ylim(min(nominal[1])-max(nominal[2]), max(nominal[1])+4*max(nominal[2]))

    ax_ratio.errorbar(up[0], down_ratio[1], yerr=down_ratio[2], xerr=down_ratio[3], color='#1446A0')
    ax_ratio.errorbar(up[0], up_ratio[1], yerr=up_ratio[2], xerr=up_ratio[3], color='#B40424')
    ax_ratio.errorbar(up[0], nominal_ratio[1], yerr=nominal_ratio[2], xerr=nominal_ratio[3], color='black')
        
    
    legend = ax_main.legend(
        title= f'Region: {region}\n\nUncertainty: {name} \n\n{MC}\n', loc='best')
    legend.get_frame().set_linewidth(0.0)

    
    # Additional settings for clarity
    ax_ratio.set_xlabel(Xaxis)
    ax_ratio.set_ylabel('Ratio')
    
    up_ratio = min(max(nominal_ratio[1])+1.5*max(nominal_ratio[2]), 3)
    down_ratio = max(min(nominal_ratio[1])-1.5*max(nominal_ratio[2]), -1)
    
    ax_ratio.set_ylim(down_ratio, up_ratio)

    # Display the plot
    plt.show()
    if filename:
        fig.savefig(filename+name+".pdf", bbox_inches = 'tight')
    plt.tight_layout()
    return fig

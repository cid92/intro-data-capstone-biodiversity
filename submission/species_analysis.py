import pandas as pd
from matplotlib import pyplot as plt

# Loading the Data
species = pd.read_csv('species_info.csv')

# Inspecting the DataFrame
print species.head()
species_type = species.category.unique()
species_count = species.scientific_name.nunique()
print 'There are '+ str(species_count)+' species of flora and fauna in the data\n'

conservation_statuses = species.conservation_status.unique()

# Analyze Species Conservation Status
conservation_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index()

# print conservation_counts

# Analyze Species Conservation Status II
species.fillna('No Intervention', inplace = True)

conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()

species_status_count = conservation_counts_fixed.scientific_name.sum()

print 'The total number of species based on conversation status is '+str(species_status_count)+'\n'

# Check for duplicate species
duplicated_species = species[species.scientific_name.duplicated(keep = False)].reset_index()
duplicated_species['status_check']  = True
# Check for species with more than one conservation_status
print 'Types of species that have more than one conservation status'
i = 0 
for x in range(len(duplicated_species)):
    check_status = duplicated_species[duplicated_species.scientific_name == duplicated_species.iloc[x,2]].conservation_status.duplicated(keep = False).all()
    if check_status == False:
        print duplicated_species.scientific_name.loc[x]

duplicated_species[duplicated_species.status_check == False]


# Plotting Conservation Status by Species
protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')
print '\n'
print protection_counts
plt.figure(figsize=(10, 4))
ax = plt.subplot()
rects = ax.bar(range(len(protection_counts)),
protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]

def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.005*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')

autolabel(rects)

plt.show()



species['is_protected'] = species.conservation_status != 'No Intervention'

#category_counts = species.groupby(['category', 'is_protected'])\
#.scientific_name.count().reset_index()

category_counts = species.groupby(['category','is_protected']).scientific_name.nunique().reset_index()


# print category_counts.head()

category_pivot = category_counts.pivot(columns='is_protected', index='category'
                                       , values='scientific_name').reset_index()

category_pivot.columns = ['category', 'not_protected', 'protected']

category_pivot['percent_protected'] = (category_pivot.protected / 
              (category_pivot.protected + category_pivot.not_protected)*100)
round2dec = lambda x: round(x,1)
category_pivot['percent_protected'] = category_pivot.percent_protected.apply(round2dec)
print category_pivot

#Indexing the data for chi table

amphibian_info = category_pivot[(category_pivot.category == 'Amphibian')]

fish_info = category_pivot[(category_pivot.category == 'Fish')]

bird_info = category_pivot[(category_pivot.category == 'Bird')]

mammal_info = category_pivot[(category_pivot.category == 'Mammal')]

np_info = category_pivot[(category_pivot.category == 'Nonvascular Plant')]

reptile_info = category_pivot[(category_pivot.category == 'Reptile')]

vp_info = category_pivot[(category_pivot.category == 'Vascular Plant')]

#Determining the contingencies
contingency = [[mammal_info.iloc[0,2],mammal_info.iloc[0,1]],[bird_info.iloc[0,2],bird_info.iloc[0,1]]]
print '\n'
print contingency
print '\n'
from scipy.stats import chi2_contingency
chi2, pval, dof, expected = chi2_contingency(contingency)

print pval
print '\n'

contingency2 = [[mammal_info.iloc[0,2],mammal_info.iloc[0,1]],[reptile_info.iloc[0,2],reptile_info.iloc[0,1]]]

chi2, pval_reptile_mammal, dof, expected = chi2_contingency(contingency2)

print pval_reptile_mammal
print '\n'


contingency3 = [[amphibian_info.iloc[0,2],amphibian_info.iloc[0,1]],[reptile_info.iloc[0,2],reptile_info.iloc[0,1]]]

chi2, pval_amphibian_reptile, dof, expected = chi2_contingency(contingency3)

print pval_amphibian_reptile
print 'No significant difference between amphibians and reptiles \n'

contingency4 = [[np_info.iloc[0,2],np_info.iloc[0,1]],[vp_info.iloc[0,2],vp_info.iloc[0,1]]]



chi2, pval_non_vascular, dof, expected = chi2_contingency(contingency4)

print pval_non_vascular
print '''Are nonvascular plants more endangered than vascular plants? No \n'''

contingency5 = [[amphibian_info.iloc[0,2],amphibian_info.iloc[0,1]],[bird_info.iloc[0,2],bird_info.iloc[0,1]]]

chi2, pval_amphibian_bird, dof, expected = chi2_contingency(contingency5)

print pval_amphibian_bird
print 'No significant difference between amphibians and birds \n'

contingency6 = [[fish_info.iloc[0,2],fish_info.iloc[0,1]],[bird_info.iloc[0,2],bird_info.iloc[0,1]]]

chi2, pval_fish_bird, dof, expected = chi2_contingency(contingency6)

print pval_fish_bird
print 'No significant difference between fish and birds \n'

species = pd.read_csv('species_info.csv')
species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]

observations = pd.read_csv('observations.csv')

sheep_observations = observations.merge(sheep_species)

obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()

plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park['park_name'])),obs_by_park['observations'])
ax.set_xticks(range(len(obs_by_park['park_name'])))
ax.set_xticklabels(obs_by_park['park_name'])
ax.set_ylabel('Number of Observations')
ax.set_title('Observations of Sheep per Week')
plt.show()

#Sample size for the foot and mouth disease study
baseline = 15
minimum_detectable_effect = 33.33
sample_size_per_variant = 850
yellowstone_weeks_observing = 1.72
bryce_weeks_observing = 3.5

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
with open("css/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

# try:
    last_update = pd.read_csv("data/last_update.csv")
    st.markdown("Terakhir Update " + last_update["0"][0])
    repo = pd.read_csv("data/repo.csv")
    wilkerstat = pd.read_csv("data/wilkerstat.csv")
    # st.markdown("test")
    if wilkerstat["nm_project"][0].astype(str).startswith("000"):
        wilkerstat['idsubsls'] = wilkerstat['iddesa'].astype(
            str)+wilkerstat['nm_project'].astype(str)
    else:
        wilkerstat['idsubsls'] = wilkerstat['iddesa'].astype(
            str)+"000"+wilkerstat['nm_project'].astype(str)
    # wilkerstat_subsls['idsubsls'] = wilkerstat_subsls['idsubsls'].astype(str)    
    repo_subsls = pd.DataFrame(repo.iloc[:, [0, 7, 22, 25]])
    repo_subsls['idsubsls'] = repo_subsls['idsubsls'].astype(str)
    
    data_merge = wilkerstat.merge(repo_subsls, how="left", on='idsubsls')
    data_merge['nama_pml'] = data_merge['nama_pml'].fillna("")
    new_pml = pd.read_excel("data/daftar pml.xlsx").iloc[:, [1,2]]
    new_pml['idsubsls'] = new_pml['idsubsls'].astype(str)
    data_merge = data_merge.merge(new_pml, how="left", on='idsubsls') 
    
    data_merge = data_merge.loc[:,['idsubsls','deskripsi_project','nama', 'nama_krt','jumlah_art_tani','subsektor','user_creator_nama','nama_pml_new']]
    
    
    col1,col2 = st.columns([2,1])
    pmls = col1.multiselect('Filter by PML', ['Muhammad Bohari Rahman S.Stat.', 'Nadya Husna S.Tr.Stat.','Muhammad Ikhwani' ,'Muhammad Fachry Nazuli S.Tr.Stat.', 'Ema Juniati SST','Hera Lestari S.Si','Iryani','Chalida Rahmi SE, M.M.','Yusra S.E','Salviyana Nurdin A.Md','Suci Maulida SST'],['Muhammad Bohari Rahman S.Stat.', 'Nadya Husna S.Tr.Stat.','Muhammad Ikhwani' ,'Muhammad Fachry Nazuli S.Tr.Stat.', 'Ema Juniati SST','Hera Lestari S.Si','Iryani','Chalida Rahmi SE, M.M.','Yusra S.E','Salviyana Nurdin A.Md','Suci Maulida SST'])
    
    try:
        filterpml = ''
        for pml in pmls:
            filterpml = filterpml +"'"+ pml+"', "
        filterpml = filterpml[:-2]   
    except: 
        st.markdown("PML Belum dipilih")
        
    lebih2 = col2.multiselect('Filter', ['ART Tani > 1', 'Hanya SubSLS yang berbeda dengan Repo'], ['ART Tani > 1', 'Hanya SubSLS yang berbeda dengan Repo'])
    # col2.markdown(lebih2)]
    
    wilkerstat_sum = wilkerstat.groupby(['idsubsls'])['jumlah_art_tani'].sum()
    wilkerstat_count = wilkerstat.groupby(
        ['idsubsls'])['jumlah_art_tani'].count()
    wilkerstat_subsls = pd.DataFrame(
        {'jumlah_tagging': wilkerstat_count, 'jumlah_art_tani': wilkerstat_sum})
    wilkerstat_subsls.index.name = 'idsubsls'
    wilkerstat_subsls.reset_index(inplace=True)
    data_merge_repo = repo_subsls.merge(wilkerstat_subsls, how="left", on='idsubsls')
    data_merge_repo['jumlah_tagging'] = data_merge_repo['jumlah_tagging'].fillna(0).astype(int)
    data_merge_repo['jumlah_art_tani'] = data_merge_repo['jumlah_art_tani'].fillna(0).astype(int)
    # st.markdown("test")
    data_merge_repo_bermasalah = data_merge_repo.query("b305 != jumlah_art_tani")
    # st.table(data_merge_repo_bermasalah)
    
    
    data_merge = data_merge.query("nama_pml_new in ("+filterpml+")")
    if 'ART Tani > 1' in lebih2:
        data_merge = data_merge.query("jumlah_art_tani > 1")
    
    try:
        if 'Hanya SubSLS yang berbeda dengan Repo' in lebih2:
            
            filteridsubsls = ''
            for idsub in data_merge_repo_bermasalah['idsubsls']:
                filteridsubsls = filteridsubsls +"'"+ idsub +"', "
            filteridsubsls = filteridsubsls[:-2]   
            data_merge = data_merge.query(f"idsubsls in ({filteridsubsls})")
            
            # st.markdown(filteridsubsls)
    except: 
        st.markdown("PML Belum dipilih")
    daftar_sls = data_merge['idsubsls'].drop_duplicates()
    if  len(daftar_sls) > 0:   
        # st.markdown(daftar_sls)
        
        filtersls = col2.selectbox('Pilih Sub SLS', [j for i in [['Semua SubSLS'], daftar_sls] for j in i] )
        st.markdown(filtersls == 'Semua SubSLS')
        if (filtersls == 'Semua SubSLS'):
            filteridsubsls = ''
            for idsub in daftar_sls:
                filteridsubsls = filteridsubsls +"'"+ idsub +"', "
            filteridsubsls = filteridsubsls[:-2]   
            data_merge = data_merge.query(f"idsubsls in ({filteridsubsls})")
            # data_merge = data_merge.query(f"idsubsls in ({daftar_sls})")
        else:
            data_merge = data_merge.query(f"idsubsls == '{filtersls}'")
    st.table(data_merge.reset_index(drop=True))
# except:
#     st.markdown("Data Belum di update")
import folium
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import geojson
# import pprint as pp
# python -m streamlit run app.py

from geojson import Point, Feature, FeatureCollection, dump


st.set_page_config(layout="wide")
with open("css/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

# try:
    # data_sbr_1 = pd.read_excel("data/part 1_direktori_usaha_template_upload_edit.xlsx")
    # data_sbr_2 = pd.read_excel("data/part 2_direktori_usaha_template_upload_edit.xlsx")
    # data_sbr_3 = pd.read_excel("data/part 3_direktori_usaha_template_upload_edit.xlsx")
    # data_sbr_4 = pd.read_excel("data/part 4_direktori_usaha_template_upload_edit.xlsx")
    # data_sbr_5 = pd.read_excel("data/part 5_direktori_usaha_template_upload_edit.xlsx")

    # data_sbr_all = pd.concat([data_sbr_1,data_sbr_2,data_sbr_3,data_sbr_4,data_sbr_5])
    # @st.cache_data
    kode_wilayah = pd.read_excel("data/kode_wilayah.xlsx")
    # print(data_sbr_all['kddesa'])
    # data_sbr_all = data_sbr_all[(data_sbr_all['kdkec']==10) & (data_sbr_all['kddesa']==22)]

    read_data = 0
    st.markdown("")
    col1,col2,col3 = st.columns([1,1,4])
    col1.link_button("Download Data SBR", "http://s.bps.go.id/dataSBR1174")
    col1,col2,col3 = st.columns([1,1,2])
    filter_kecamatan = col1.selectbox("Kecamatan",['SEMUA']+list(dict.fromkeys(kode_wilayah['kecamatan'])))
    if filter_kecamatan != "SEMUA" :
        filter_desa = col2.selectbox("Desa",['SEMUA']+list(kode_wilayah[kode_wilayah['kecamatan']==filter_kecamatan]['desa']))
        if filter_desa != "SEMUA" :
            kode_desa = kode_wilayah[kode_wilayah['kecamatan']==filter_kecamatan][kode_wilayah['desa']==filter_desa]
            search_query = col3.text_input("Cari Usaha", value="")
            # print(kode_desa.reset_index()['kode'][0])
            read_data = 1
            kddesa = kode_desa.reset_index()['kode'][0]
            data_sbr_all = pd.read_excel("data/desa/"+str(kddesa)+".xlsx")
    
    if filter_kecamatan == "SEMUA" or filter_desa == "SEMUA": 
        read_data = 0

    if read_data == 1:
        data_sbr = data_sbr_all
        data_sbr_map = data_sbr[data_sbr['latitude'].notnull()]

        with open('data/geojson/'+str(kddesa)+'.geojson', 'r') as file:
            geojson_data = geojson.load(file)

        # print(geojson_data["features"][0])
        # print(geojson_data["features"][0]["properties"]["iddesa"])


        # print(data_sbr_all["kdkec"])
        st.markdown("")
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown("Jumlah Usaha")
        col1.markdown(len(data_sbr_all[data_sbr_all['nama_usaha'].str.contains(search_query, case=False)]))
        col2.markdown("Jumlah Usaha Dengan Titik")
        col2.markdown(len(data_sbr_map[data_sbr_map['nama_usaha'].str.contains(search_query, case=False)]))
        # col3.markdown("Jumlah Usaha Duplikat")
        # col3.markdown(len(data_sbr_all))
        # col4.markdown("Jumlah ")
        # col4.markdown(len(data_sbr_all))

    

        
        connecticute_center = (data_sbr_map.reset_index()['latitude'][5], data_sbr_map.reset_index()['longitude'][5])

        map = folium.Map(location=connecticute_center, zoom_start=15)

        folium.GeoJson(geojson_data).add_to(map)
        
        if search_query != "":
            # data_sbr_search = data_sbr_map[data_sbr_map['nama_usaha'].str.contains(search_query)]
            # print('text')
            data_sbr_search = data_sbr_map[data_sbr_map['nama_usaha'].str.contains(search_query, case=False)]
            # print(len(data_sbr_search))
            if len(data_sbr_search) > 0 :
                for index, usaha in data_sbr_search.iterrows():

                    iframe = folium.IFrame(usaha.loc['nama_usaha'].replace("<","(").replace(">",")"))
                    popup = folium.Popup(iframe, min_width=200, max_width=300)
                    location = (usaha['latitude'], usaha['longitude'])
                    folium.Marker(location, popup=popup).add_to(map)
        else:
            for index, usaha in data_sbr_map.iterrows():

                iframe = folium.IFrame(usaha.loc['nama_usaha'].replace("<","(").replace(">",")"))
                popup = folium.Popup(iframe, min_width=200, max_width=300)
                location = (usaha['latitude'], usaha['longitude'])
                folium.Marker(location, popup=popup).add_to(map)
        st_folium(map,  use_container_width=True)




        display_table = """
                    <table>
                        <thead>
                            <tr>
                                <th>No</th>
                                <th>idsbr</th>
                                <th>Nama Usaha</th>
                                <th>Alamat</th>
                                <th>Keberadaan Usaha</th>
                                <th>idsbr_master</th>
                                <th>Sumber Profiling</th>
                                <th>Catatan Profiling</th>
                            </tr>
                        </thead>
                        <tbody>
                        """

        table_row = ""
        
        i = 0
        if search_query != "":
            data_sbr_table = data_sbr_all[data_sbr_all['nama_usaha'].str.contains(search_query, case=False)]
        else: 
            data_sbr_table =  data_sbr_all

        for idx in data_sbr_table.index:
            i = i+1
            color_status = "green"
            # if data_merge['b305'][idx] == data_merge['jumlah_art_tani'][idx]:
            #     status = "Repo sama dengan Wilkerstat"
            #     color_status = "green"
            # else: 
            #     status = "Repo berbeda dengan Wilkerstat"
            #     color_status = "red"
            if data_sbr_all['keberadaan_usaha'][idx] > 0 :
                table_row = table_row + f"<tr><td>{i}</td><td>{data_sbr_all['idsbr'][idx]}</td><td>{data_sbr_all['nama_usaha'][idx].replace("<","(").replace(">",")")}</td><td>{data_sbr_all['alamat'][idx]}</td><td>{int(data_sbr_all['keberadaan_usaha'][idx])}</td><td>{data_sbr_all['idsbr_master'][idx]}</td><td>{data_sbr_all['sumber_profiling'][idx]}</td><td><span>{data_sbr_all['catatan_profiling'][idx]}</span></td></tr>"
            else : 
                table_row = table_row + f"<tr><td>{i}</td><td>{data_sbr_all['idsbr'][idx]}</td><td>{data_sbr_all['nama_usaha'][idx].replace("<","(").replace(">",")")}</td><td>{data_sbr_all['alamat'][idx]}</td><td></td><td>{data_sbr_all['idsbr_master'][idx]}</td><td>{data_sbr_all['sumber_profiling'][idx]}</td><td><span>{data_sbr_all['catatan_profiling'][idx]}</span></td></tr>"
        # st.markdown(table_row)    
        display_tables = f"{display_table}{table_row}</tbody></table>"
        st.markdown(display_tables, unsafe_allow_html=True)

    
#     last_update = pd.read_csv("data/last_update.csv")
#     st.markdown("Terakhir Update " + last_update["0"][0])
#     repo = pd.read_csv("data/repo.csv")
#     wilkerstat = pd.read_csv("data/wilkerstat.csv")

#     if wilkerstat["nm_project"][0].astype(str).startswith("000"):
#         wilkerstat['idsubsls'] = wilkerstat['iddesa'].astype(
#             str)+wilkerstat['nm_project'].astype(str)
#     else:
#         wilkerstat['idsubsls'] = wilkerstat['iddesa'].astype(
#             str)+"000"+wilkerstat['nm_project'].astype(str)
#     col1, col2, col3, col4 = st.columns(4)
#     col1.markdown("Jumlah SLS/Non SLS Repo")
#     col1.markdown(len(repo))
#     col2.markdown("Jumlah UTP (R305) Repo")
#     col2.markdown(sum(repo['b305']))
#     col3.markdown("Jumlah Project Wilkerstat")
#     col3.markdown(len(wilkerstat.groupby('idsubsls').count()))
#     col4.markdown("Jumlah ART Pertanian")
#     col4.markdown(sum(wilkerstat['jumlah_art_tani']))

#     wilkerstat_sum = wilkerstat.groupby(['idsubsls'])['jumlah_art_tani'].sum()
#     wilkerstat_count = wilkerstat.groupby(
#         ['idsubsls'])['jumlah_art_tani'].count()
#     wilkerstat_subsls = pd.DataFrame(
#         {'jumlah_tagging': wilkerstat_count, 'jumlah_art_tani': wilkerstat_sum})
#     wilkerstat_subsls.index.name = 'idsubsls'
#     wilkerstat_subsls.reset_index(inplace=True)
#     repo_subsls = pd.DataFrame(repo.iloc[:, [0, 7, 22, 25]])
#     repo_subsls['idsubsls'] = repo_subsls['idsubsls'].astype(str)
#     wilkerstat_subsls['idsubsls'] = wilkerstat_subsls['idsubsls'].astype(str)
#     new_pml = pd.read_excel("data/daftar pml.xlsx").iloc[:, [1,2]]
#     new_pml['idsubsls'] = new_pml['idsubsls'].astype(str)
#     # st.table(new_pml)
#     # wilkerstat_subsls['jumlah_tagging'] = wilkerstat_subsls['jumlah_tagging'].astype(int)
#     # wilkerstat_subsls['jumlah_art_tani'] = wilkerstat_subsls['jumlah_art_tani'].astype(int)
#     col1 = st.container()
#     pmls = col1.multiselect('Filter by PML', ['Muhammad Bohari Rahman S.Stat.', 'Nadya Husna S.Tr.Stat.','Muhammad Ikhwani' ,'Muhammad Fachry Nazuli S.Tr.Stat.', 'Ema Juniati SST','Hera Lestari S.Si','Iryani','Chalida Rahmi SE, M.M.','Yusra S.E','Salviyana Nurdin A.Md','Suci Maulida SST'],['Muhammad Bohari Rahman S.Stat.', 'Nadya Husna S.Tr.Stat.','Muhammad Ikhwani' ,'Muhammad Fachry Nazuli S.Tr.Stat.', 'Ema Juniati SST','Hera Lestari S.Si','Iryani','Chalida Rahmi SE, M.M.','Yusra S.E','Salviyana Nurdin A.Md','Suci Maulida SST'])
#     try:
#         filterpml = ''
#         for pml in pmls:
#             filterpml = filterpml +"'"+ pml+"', "
#         filterpml = filterpml[:-2]   
#     except: 
#         st.markdown("PML Belum dipilih")
#     data_merge = repo_subsls.merge(wilkerstat_subsls, how="left", on='idsubsls')
#     data_merge['jumlah_tagging'] = data_merge['jumlah_tagging'].fillna(0).astype(int)
#     data_merge['jumlah_art_tani'] = data_merge['jumlah_art_tani'].fillna(0).astype(int)
#     data_merge = data_merge.merge(new_pml, how="left", on='idsubsls') 
#     # st.table(data_merge)
#     data_merge = data_merge.query("nama_pml_new in ("+filterpml+")")
#     # st.container().table(data_merge)
    
#     display_table = """
#                 <table>
#                     <thead>
#                         <tr>
#                             <th>No</th>
#                             <th>ID SubSLS</th>
#                             <th>Nama SLS</th>
#                             <th>UTP Repo (R305)</th>
#                             <th>Jumlah Tagging</th>
#                             <th>Jumlah ART Tani Wilkerstat</th>
#                             <th>Nama PML</th>
#                             <th>Status</th>
#                         </tr>
#                     </thead>
#                     <tbody>
#                     """

#     table_row = ""
#     i = 0
#     for idx in data_merge.index:
#         i = i+1
#         if data_merge['b305'][idx] == data_merge['jumlah_art_tani'][idx]:
#             status = "Repo sama dengan Wilkerstat"
#             color_status = "green"
#         else: 
#             status = "Repo berbeda dengan Wilkerstat"
#             color_status = "red"
#         table_row = table_row + f"<tr><td>{i}</td><td>{data_merge['idsubsls'][idx]}</td><td>{data_merge['nmsls'][idx]}</td><td>{data_merge['b305'][idx]}</td><td>{data_merge['jumlah_tagging'][idx]}</td><td>{data_merge['jumlah_art_tani'][idx]}</td><td>{data_merge['nama_pml_new'][idx]}</td><td><span style='color:{color_status};'>{status}</span></td></tr>"
#     # st.markdown(table_row)    
#     display_tables = f"{display_table}{table_row}</tbody></table>"
#     st.markdown(display_tables, unsafe_allow_html=True)
# # except:
# #     st.markdown("Data Belum di update")


#### Export Data Desa
    # print(int(str(kode_wilayah["kode"][50])[4:7]))
    # for index, desa in kode_wilayah.iterrows():
    #     kdkec = int(str(desa["kode"])[4:7])
    #     kddesa = int(str(desa["kode"])[7:])
    #     if kddesa < 10:
    #         namafile = "data/desa/11740"+str(kdkec)+"00"+str(kddesa)+".xlsx"
    #     else:
    #         namafile = "data/desa/11740"+str(kdkec)+"0"+str(kddesa)+".xlsx"
    #     data_sbr_export = data_sbr_all[(data_sbr_all['kdkec']==kdkec) & (data_sbr_all['kddesa']==kddesa)]
    #     data_sbr_export.to_excel(namafile, sheet_name=desa["desa"], index=False)
        # print(int(str(desa["kode"])[7:]))

    #### Export Data per kecamatan
    # kdkec = 30

    # data_sbr_export = data_sbr_all[(data_sbr_all['kdkec']==kdkec) & (data_sbr_all['kddesa']==1)]
    # namafile = "data/11740"+str(kdkec)+".xlsx"
    # data_sbr_export.to_excel(namafile, sheet_name=kode_wilayah["desa"][50], index=False)  
    # for  i in range(2,19):
    #     with pd.ExcelWriter(namafile, mode='a') as writer:  
    #         data_sbr_export = data_sbr_all[(data_sbr_all['kdkec']==kdkec) & (data_sbr_all['kddesa']==i)]
    #         data_sbr_export.to_excel(writer, sheet_name=kode_wilayah["desa"][i+49], index=False)

    #Export Data geojson
    # for i in range(0,68):

        #     datajson = {
        #                 "type": "FeatureCollection",
        #                 "name": f"{geojson_data["features"][i]["properties"]["iddesa"]}",
        #                 "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        #                 "features": [geojson_data["features"][i]]}
        # # print(datajson)

        #     with open('data/geojson/'+str(geojson_data["features"][i]["properties"]["iddesa"])+'.geojson', 'w') as f:
        #         dump(datajson, f)
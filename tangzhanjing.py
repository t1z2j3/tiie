'''我的项目'''
import streamlit as st
from PIL import Image
import media_tool
from pydub import AudioSegment
from pydub.playback import play

page = st.sidebar.radio('我的主页',['网页介绍','我的图片处理工具','我的智能词典','我的留言区',"链接分享","音乐处理"])
def page_1():
    '''网页介绍'''
    st.write("这个网站以后就是咱们几个的小根据地了！！")
    st.write("！！！记住，是你们义父建的网站！！！")
    st.image("1.gif")

def page_2():
    '''我的图片处理工具'''
    st.write(":sunglasses:图片处理小程序:sunglasses:")
    uploaded_file = st.file_uploader("上传图片",type=['png','jpeg','jpg'])
    if uploaded_file:
        file_name = uploaded_file.name
        file_type = uploaded_file.type
        file_size = uploaded_file.size
        img = Image.open(uploaded_file)
        tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(["原图","改色1","改色2","改色3","改色4","黑白图"])
        with tab1:
            st.image(img)
        with tab2:
            st.image(img_change(img,2,0,1))
        with tab3:
            st.image(img_change(img,0,2,1))
        with tab4:
            st.image(img_change(img,1,0,2))
        with tab5:
            st.image(img_change(img,2,1,0))
        with tab6:
            st.image(img.convert("L"))
def page_3():
    '''我的智能词典'''
    st.write('智能词典')
    with open('words_space.txt','r',encoding='utf-8') as f:
        words_list = f.read().split('\n')
    for i in range(len(words_list)):
        words_list[i] = words_list[i].split('#')
    words_dict = {}
    for i in words_list:
        words_dict[i[1]] = [int(i[0]),i[2]]
    with open('check_out_times.txt','r',encoding='utf-8') as f:
        times_list = f.read().split('\n')
    for i in range(len(times_list)):
        times_list[i] = times_list[i].split('#')
    times_dict = {}
    for i in times_list:
        times_dict[int(i[0])] = int(i[1])
    word = st.text_input('请输入要查询的单词')
    if word in words_dict:
        st.write(words_dict[word])
        n = words_dict[word][0]
        if n in times_dict:
            times_dict[n] += 1
        else:
            times_dict[n] = 1
        with open('check_out_times.txt','w',encoding='utf-8') as f:
            message = ''
            for k,v in times_dict.items():
                message+=str(k)+'#'+str(v)+'\n'
            message = message[:-1]
            f.write(message)
        st.write('查询次数：',times_dict[n])

def page_4():
    '''我的留言区'''
    st.write('我的留言区')
    with open('leave_messages.txt','r',encoding='utf-8') as f:
        messages_list = f.read().split('\n')
    for i in range(len(messages_list)):
        messages_list[i] = messages_list[i].split('#')
    for i in messages_list:
        if i[1] == '汤占京（义父）':
            with st.chat_message('💯'):
                st.write(i[1],":",i[2])
        elif i[1] == '义子一号':
            with st.chat_message('☕'):
                st.write(i[1],":",i[2])   
    name = st.selectbox('我是...',['汤占京（义父）','义子一号'])
    new_message= st.text_input('想要说的话...')
    if st.button('留言'):
        messages_list.append([str(int(messages_list[-1][0])+1),name,new_message])
        with open('leave_messages.txt','w',encoding='utf-8') as f:
            message = ''
            for i in messages_list:
                message += i[0]+'#'+i[1]+'#'+i[2]+'\n'
            message = message[:-1]
            f.write(message)
    
def page_5():
    '''链接分享'''
    for i in range(5):
        st.write(' ')
    st.link_button('离线版钢铁雄心四下载网址(夸克网盘)', 'https://pan.quark.cn/s/d3c686e3cfa0')
    for i in range(10):
        st.write(' ')
    st.link_button('Steam官网', 'https://store.steampowered.com/')
    for i in range(10):
        st.write(' ')
    st.link_button('抖音', 'https://www.douyin.com/')
    
def page_6():
    '''音乐处理'''
    an = st.file_uploader("上传音乐",type=['mp3'])
    if an:
        sound = AudioSegment.from_mp3(an)
        times = int(sound.duration_seconds)
        sound = sound.set_channels(2)
        sound_channels = sound.split_to_mono()
        left_sound = sound_channels[0]
        right_sound = sound_channels[1]
        number1,number2 = st.slider('音轨1：', 0, times,(0,0))
        number3,number4 = st.slider('音轨2：', 0, times,(0,0))
        st.write('音轨1：', number1)
        st.write('音轨2：', number2)
        if st.button('处理'):
            sound = sound.set_channels(2)
            sound_channels = sound.split_to_mono()
            left_sound = sound_channels[0]
            right_sound = sound_channels[1]
            left =AudioSegment.empty()
            left += left_sound[0:number1*1000].apply_gain(-120.0)
            left += left_sound[number1*1000:number2*1000].fade_out(500).fade_in(500)
            left += left_sound[number2*1000:times*1000].apply_gain(-120.0)
            right = AudioSegment.empty()
            right += right_sound[0:number3*1000].apply_gain(-120.0)
            right += right_sound[number3*1000:number4*1000].fade_out(500).fade_in(500)
            right += right_sound[number4*1000:times*1000].apply_gain(-120.0)
            new_sound = AudioSegment.from_mono_audiosegments(left,right)
            new_sound.export("新音乐.mp3",format = "mp3")
            st.download_button(label = "新音乐下载",data = "新音乐.mp3",file_name = "新音乐.mp3")
            if st.button("播放"):
                st.music(new_sound)
def img_change(img,rc,gc,bc):
    width,height = img.size
    img_array = img.load()
    for x in range(width):
        for y in range(height):
            r = img_array[x,y][rc]
            g = img_array[x,y][gc]
            b = img_array[x,y][bc]
            img_array[x,y] = (r,g,b)
    return img
if page == '网页介绍':
    page_1()
elif page == '我的图片处理工具':
    page_2()
elif page == '我的智能词典':
    page_3()
elif page == '我的留言区':
    page_4()
elif page == '链接分享':
    page_5()
elif page == '音乐处理':
    page_6()   
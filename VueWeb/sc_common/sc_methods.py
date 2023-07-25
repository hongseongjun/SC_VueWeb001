import os
from uuid import uuid4
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from pydub import AudioSegment
#import numpy as np                 #Error in Apache2(mod-wsgi) of Django Web Server

###########################################################################################################
#   Part-I. Upload File Directory Management
###########################################################################################################
# 1. Sample Image of Target Species : target_species/images
def get_sample_image_path(instance, filename):
    #print('get_sample_image_path *********************')
    file_ext = os.path.splitext(filename)[-1].lower()
    file_name = 'target_species/images/{0}{1}'.format(instance.name, file_ext)
    return file_name

# 2. Sample Sound of Target Species : Target_Species/Sounds
def get_sample_sound_path(instance, filename):
    #print('get_sample_sound_path *********************')
    file_ext = os.path.splitext(filename)[-1].lower()
    file_name = 'target_species/sounds/{0}{1}'.format(instance.name, file_ext)
    return file_name

# 3. Pure Sound Collection for Target Species : Pure_Collect/Sect/Type/Name
def get_collect_sound_path(instance, filename):
    while(True) :
        # 1) Make Some Unique Sound File by uuid4().hex
        uuid_name = uuid4().hex
        sound_sect = instance.species.name
        sound_type = instance.species_sub.name
        sound_name = instance.target.name

        # 2) Check Unique for Previous Made Sound File Until No Duplicating
        #file_ext = os.path.splitext(filename)[-1].lower()
        file_name = 'pure_collect/{0}/{1}/{2}/{3}'.format(sound_sect, sound_type, sound_name, uuid_name)
        if not os.path.exists(file_name):
            return file_name

# 4. 공지사항 첨부파일 경로설정
def get_notice_file_path(instance, filename):
    uuid_name = uuid4().hex
    file_year = datetime.now().strftime('%Y')   #file_date = datetime.now().strftime('%Y/%m/%d')
    file_name = 'board_notice/{0}/{1}'.format(file_year, uuid_name)
    return file_name

# 5. 자유게시판 첨부파일 경로설정
def get_free_file_path(instance, filename):
    uuid_name = uuid4().hex
    file_year = datetime.now().strftime('%Y')   #file_date = datetime.now().strftime('%Y/%m/%d')
    file_name = 'board_free/{0}/{1}'.format(file_year, uuid_name)
    return file_name

# 6. 자료실 첨부파일 경로설정
def get_data_file_path(instance, filename):
    uuid_name = uuid4().hex
    file_year = datetime.now().strftime('%Y')   #file_date = datetime.now().strftime('%Y/%m/%d')
    file_name = 'data_room/{0}/{1}'.format(file_year, uuid_name)
    return file_name


###########################################################################################################
#   Part-II. SC-Common Processing Management
###########################################################################################################

# 1. 특정 사이트 접근근지 설정
def protected_file(request, path, document_root=None):
    messages.error(request, "접근 불가")
    return redirect('/')

# 2. 이미지, 사운드 파일 포멧 검증 : For Target Player File
def validate_file(fname, format):
    image = ['.jpg', '.jpeg', '.png']
    sound = ['.wav', '.mp3', '.ogg']
    try:
        ext = os.path.splitext(fname)[-1].lower()
        if format == 'sound':
            if ext in sound: return
            else: raise forms.ValidationError('정확한 포멧의 사운드 [jpg, jpeg, png]를 입력해주세요.')
        else :
            if ext in image: return
            else: raise forms.ValidationError('정확한 포멧의 이미지 [wav, mp3]를 입력해주세요.')
    except Exception:
        raise forms.ValidationError('적절한 첨부파일 포멧이 아닙니다. 다시 입력하세요.')

# 3. 사운드 파일 정규화 처리 및 음향 기본정보 DB 등록 : For Collect Sound File
def normalize_sound(instance):
    if instance.dstate: return                                  # 삭제된 파일인 경우
    audio = AudioSegment.from_wav(instance.sfile.path)          # AudioSegment 객체
    audio = audio.set_channels(1)                               # Mono Channel
    audio = audio.set_frame_rate(44100)                         # Sampling Rate
    audio = audio.set_sample_width(2)                           # 샘플 크기(byte)
    audio = audio.normalize(0.1)                                # 채집음원 정규화(headroom=0.1), 2021.04.16
    audio.export(instance.sfile.path, format="wav")             # 채집음원 저장
    instance.srate = audio.frame_rate                           # 샘플링 주기[Hz]
    instance.schannel = audio.channels                          # 채널 수
    instance.swidth = audio.sample_width                        # 샘플 크기(byte)
    instance.ssize = round(len(audio.raw_data) / 1000000, 2)    # 음원크기[Mb]
    instance.sduration = round(audio.duration_seconds / 60, 2)  # 재생시간(분)
    #----------------------------------------------------------------------------------------
    #instance.snr = check_snr_rtn(audio, 100, 6)                # SNR[dB], 2021.09.03, Error in [Numpy Package Import]
    # ----------------------------------------------------------------------------------------
    instance.nstate = True                                      # 정규화 상태정보 변경
    instance.save()                                             # 음원정보 저장

# 4. 5초 분량으로 사운드 파일 정규화 처리 : For Target Player File
def normalize_sound_5sec(instance):
    # 1) Get Sound File
    fext = os.path.splitext(instance.soundfile.path)[1]
    if fext == '.wav' :
        audio = AudioSegment.from_wav(instance.soundfile.path)
    elif fext == '.mp3' :
        audio = AudioSegment.from_mp3(instance.soundfile.path)
    elif fext == '.ogg' :
        audio = AudioSegment.from_ogg(instance.soundfile.path)

    # 2) Normalize Sound File(5 sec)
    #print(audio.duration_seconds)
    if audio.duration_seconds > 5:
        audio = audio[0:5000]
    #audio = audio.apply_gain(-audio.max_dBFS)
    audio = audio.normalize(0.1)                                # 채집음원 정규화(headroom=0.1), 2021.04.16
    #print('**************************', fext, instance.soundfile.path)

    # 3) Save Sound
    if fext == '.wav' :
        audio.export(instance.soundfile.path, format="wav")
    elif fext == '.mp3' :       #error
        audio.export(instance.soundfile.path, format="mp3")
    elif fext == '.ogg' :       #error
        audio.export(instance.soundfile.path, format="ogg")

# 5. 음향 기본정보 DB 설정 : For Collect Sound File
def set_sound_inform(instance):
    audio = AudioSegment.from_wav(instance.sfile.path)          # AudioSegment 객체
    instance.srate = audio.frame_rate                           # 샘플링 주기[Hz]
    instance.schannel = audio.channels                          # 채널 수
    instance.swidth = audio.sample_width                        # 샘플 크기(byte)
    instance.ssize = round(len(audio.raw_data) / 1000000, 2)    # 음원크기[Mb]
    instance.sduration = round(audio.duration_seconds / 60, 2)  # 재생시간(분)
    instance.nstate = False                                     # 정규화 상태정보 변경
    instance.dstate = False                                     # 파일삭제 상태
    instance.save()

# 6. Target Player & Collect Sound 인증/불인증 처리
def certify_sc_contents(instance, state):
    # 1) Certify Target Player & Collect Sound
    instance.confirm = state        # Set Certification
    instance.save()                 # DB Update

# 7. Check Authority to Process for Target species & Sound collection of Players : state = ['target', 'sound', 'etc']
def check_authority_process(user, object, state):
    # Return Authority for Some Job
    m_Auth = 400                                                            #SC 미인증 사용자
    if state == 'target':       # 1) Check Authority for [Target species] Management
        if user == object.manager or user.is_superuser or (user.is_staff and user.level == '1'):
            m_Auth = 100  # SC 관리자-1 & 본인등록자
        elif user.is_staff and user.level == '2':
            m_Auth = 200  # SC 관리자-2
        elif user.is_staff and user.level == '3':
            m_Auth = 300  # SC-로그인 사용자
    elif state == 'sound':      # 2) Check Authority for [Sound collection] Management
        if user == object.collector or user == object.manager or user.is_superuser or (user.is_staff and user.level == '1'):
            m_Auth = 100  # SC 관리자-1 & 본인등록자
        elif user.is_staff and user.level == '2':
            m_Auth = 200  # SC 관리자-2
        elif user.is_staff and user.level == '3':
            m_Auth = 300  # SC-로그인 사용자
    else:                       # 3) Check Authority for [data_room, free, notice] Management
        if user == object.writer or user.is_superuser or (user.is_staff and user.level == '1'):
            m_Auth = 100                                                        #SC 관리자-1 & 본인등록자
        elif user.is_staff and user.level == '2':
            m_Auth = 200                                                        #SC 관리자-2
        elif user.is_staff and user.level == '3':
            m_Auth = 300                                                        #SC-로그인 사용자
    return m_Auth

# 8. 채집음원 품질평가
#*******************************************************************************************************************
#   check_snr_rtn(m_Audio, m_RmsStep, m_MaxMinNum) : Error at numpy package in Django(2021.09.01)
#   - m_Audio : AudioSegment Object of Wav File to Check
#   - m_RmsStep : RMS Range Number of m_RmsUnit to Compute m_RmsArray, (Recommend Value : 60 ~ 120)
#   - m_MaxMinNum : Min/Max Range Number to Mean, (Recommend Value : 4 ~ 10)
#   cf) m_SNRdB 척도 : a) 45[dB] 이상 : 고품질, b) 25~45[dB] : 신뢰품질, c) 15~25[dB] : 저품질, d) 15[dB] 이하 : 미신뢰
#*******************************************************************************************************************
"""
def check_snr_rtn(m_Audio, m_RmsStep, m_MaxMinNum):
    # 1) Get Source Wav Data until Max Number [44100 * 60] and Set RMS Array by [m_RmsStep] Unit
    m_WavData = np.array(m_Audio.get_array_of_samples())
    m_WavSize = m_WavData.size
    m_WavSize = m_WavSize if m_WavSize < 44100 * 60 else 44100 * 60
    m_RmsNum = int(m_WavSize / m_RmsStep)
    m_RmsArray = np.array([])

    # 2) Compute RMS Array of [m_RmsArray] and Sort It by Ascending Order
    for ii in range(m_RmsNum):
        m_RmsUnit = m_WavData[ii * m_RmsStep:(ii + 1) * m_RmsStep].astype(np.long)
        m_Rms = np.sqrt(np.mean(m_RmsUnit ** 2))
        m_RmsArray = np.append(m_RmsArray, m_Rms)
    m_RmsArray.sort()

    # 3) Compute Mean of Max & Min by [m_MaxMinNum] Unit
    m_rMin = np.mean(m_RmsArray[0:m_MaxMinNum])
    m_rMin = 32.767 if m_rMin == 0 else m_rMin
    m_rMax = np.mean(m_RmsArray[-(m_MaxMinNum + 1):-1])

    # 4) Compute Final SNR[dB] and Return It
    m_SNRdB = np.round(20 * np.log10(m_rMax / m_rMin), 2)
    return m_SNRdB
"""

import os,sys
import re
import psutil
import time


def second_time(second):
	m, s = divmod(int(second), 60)
	h, m = divmod(m, 60)
	return "%02d:%02d:%02d" % (h, m, s)

def get_conf():
	conf_fp=open('movie_cut.conf','rb')
	for line in conf_fp.readlines():
		conf_msg=line.strip().decode('UTF-8')
		if '#' not in conf_msg and conf_msg:
			index=conf_msg.index('=')
			if 'movile_path' in conf_msg:
				movile_path=conf_msg[index+1:]
			elif 'movile_cut_time_file' in conf_msg:
				movile_cut_time_file=conf_msg[index+1:]
			elif 'movie_final_path' in conf_msg:
				movie_final_path=conf_msg[index+1:]
	conf_fp.close()
	return movile_path,movile_cut_time_file,movie_final_path

def get_cut_movie_file_info(file):
	cut_movie_fp=open(file,'rb')
	movie_spilt=[]
	movie_spilt_all=[]
	for line in cut_movie_fp.readlines():
		cut_msg=line.strip().decode('gb2312')
		if '#' not in cut_msg:
			try:
				index=cut_msg.index('?')
			except:
				index=-1
			if index == -1:
				movie_spilt.append(cut_msg[0:])
			else:
				movie_spilt.append(cut_msg[0:index])
				movie_spilt.append(cut_msg[index+1:])
			movie_spilt_all.append(movie_spilt)
			movie_spilt=[]
	cut_movie_fp.close()
	return movie_spilt_all


def cut_movie(mpath,mfpath,all_second,time_list,zt_list):
	cut_filename=re.findall(r'(?<=/)(.+?)(?=\.)',mpath)
	movie_file_sum=len(all_second)
	s_time=0
	for i in range(movie_file_sum):
		# print('ffmpeg.exe -i '+mpath+' -ss ' +str(time_list[i])+' -t '+str(all_second[i])+' '+mfpath+cut_filename[0]+'_'+str(i)+'_'+zt_list[i][:20]+'.mp4' )
		movie_list=os.popen('ffmpeg.exe -i '+'"'+ mpath +'"'+' -ss ' +str(time_list[i])+' -t '+str(all_second[i])+' '+'"'+mfpath+cut_filename[0]+'_'+str(i)+'_'+zt_list[i][:20]+'.mp4'+'"' )


def time_to_second(time_list):
	all_second=[]
	for time_index in range(len(time_list)):
		if time_index!=0:
			ts=time_list[time_index-1].split(':')
			tp=time_list[time_index].split(':')
			end_time=int(tp[0])*3600 + int(tp[1])*60 + int(tp[2])
			start_time=int(ts[0])*3600 + int(ts[1])*60 + int(ts[2])
			all_second.append(end_time-start_time)
	return all_second

def main():
	mpath,movile_cut_time_file,mfpath=get_conf()
	print(mpath)
	movie_cut_list=get_cut_movie_file_info(movile_cut_time_file)
	time_list=[]
	zt_list=[]
	for time_point_index in range(len(movie_cut_list)):
			time_list.append(movie_cut_list[time_point_index][0])
			if time_point_index!=0:
				zt_list.append(movie_cut_list[time_point_index][1])
	all_second=time_to_second(time_list)
	cut_movie(mpath,mfpath,all_second,time_list,zt_list)

if __name__ == '__main__':
	main()

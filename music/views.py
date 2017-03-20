from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic import View
from .forms import UserForm
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy
from .models import Album,Song



class IndexView(generic.ListView):
	template_name='index.html'
	context_object_name='albums'
	def get_queryset(self):
		return Album.objects.all()

class SongsView(generic.ListView):
	template_name='songs_list.html'
	context_object_name='songs'
	def get_queryset(self):
		return Song.objects.all()


class DetailView(generic.DetailView):
	model=Album
	template_name='details.html'

class AlbumCreate(CreateView):
	template_name='album_form.html'
	model=Album
	fields=['artist','album_title','genre','album_logo']

class SongCreate(CreateView):
	template_name='album_form.html'
	model=Song
	fields=['album','song_title']

class AlbumUpdate(UpdateView):
	template_name='album_form.html'
	model=Album
	fields=['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
	template_name='album_form.html'
	model=Album
	
	success_url=reverse_lazy('music:index')

class UserFormView(View):
	form_class=UserForm
	template_name='registration_form.html'
	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form=self.form_class(request.POST)
		if form.is_valid():
			user=form.save(commit=False)
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user.set_password(password)
			print username

			user=form.save()
			user=authenticate(username=username,password=password)
			print user
                
			if user is not None:
				print 'in  not none'
				if user.is_active:
					print 'in is active'
					login(request,user)
					return redirect('music:index')

		return render(request,self.template_name,{'form':form})	

		

	

class SearchResults(View):
	template_name='search_page.html'
	
	def get(self,request):
		query=request.GET.get('q')
		if query:
			q_set1=Album.objects.filter(Q(album_title__icontains=query)|Q(artist__icontains=query))
			q_set2=Song.objects.filter(Q(song_title__icontains=query))
		
		return render(request,self.template_name,{'albums':q_set1,'songs':q_set2})	
# MBTI 페이지 과제 (홍진욱, 한수현)
***
# ❗️ERD

![ERD](/MBTI_likelion/ERD_MBTI.png)
[link][https://www.erdcloud.com/d/g3qNePNiy2dTTPBRq]
***
# ❗️코드 별 기능
***
# 1. 회원가입 / 로그인 / 로그아웃

##  **🫵 회원가입**

## *🍎 model*
    
    class Profile(AbstractUser):
        nickname = models.CharField(max_length=15);
        user_mbti = models.CharField(max_length=4);

        def __str__(self):
            return self.nickname
* 장고에서 기본으로 제공하는 AUTH를 이용해 User를 구성(기본 : username , password1 , password2 )
+ 다른 항목들을 추가하기 위해, AbstractUser를 이용함.
+ 한 user의 profile에 접근했을 때 닉네임으로 표기해 주기 위해 def str 을 사용했음.

## *🍊 url*

    path('signup/', views.signup, name='signup')\
* 보이는 그대로.

## *🍉 view*

    def signup(request):
        if request.method == "POST":
            form = Signupform(request.POST)
            if form.is_valid():
                    form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    login(request, user)
                    return redirect('MBTIAPP:main')
        else:
            form = Signupform()
        return render(request, 'MBTIAPP/signup.html', {'form' : form})
* POST 방식의 요청을 받으면 , 미리 작성해둔 "Signupform"을 form으로 정의해줌 => 그 후, form을 검사하고 , 저장. 저장한 데이터들을 변수들에 담음(cleaned_data.get) 

* 그 후 회원가입이 완료되면 자동으로 로그인 되게 처리 후 main 페이지로 보냄

* GET 방식일때는 (else문) signup.html을 그냥 form을 담아서 보여줌 (당연히 가입하려고 회원가입을 누른 상황이니까)

## *🍋 form*

    class Signupform(UserCreationForm):
        nickname = forms.CharField(max_length=15 ,label="닉네임", required=True)

        class Meta:
            model = Profile
            fields = ("username", "password1" , "password2", "nickname")

* 여기서 AbstractUser로 구현했기에, 연결하느라 좀 애를 먹음.

* nickname 은 기본 AUTH USER에 없기에 따로 추가해줬음.

* form을 템플릿 상에서 보여줄 때, 어떤 필드를 보여줄지를 나열함.

## *🍏 templates*

    <form method="post" action="{% url 'MBTIAPP:signup' %}">
        {% csrf_token %}
        {% include "MBTIAPP/form_errors.html" %}
* 템플릿은 너무 길어서 핵심만 첨부.

* 회원가입을 하고 정보를 보내니, POST 방식으로, signup의 이름을 가진 url으로 보냄.

* 보안을 위해 csrf_token , form_errors.html 만들어서 오류처리 (장고 내장기능) => 점프 투 장고 참고

****

##  **🫵 로그인**

## *🍊 url*

    path('login/', auth_views.LoginView.as_view(template_name='MBTIAPP/login.html'),name='login'),

* 장고에 내장되어 있는, LoginView를 import해서 사용.

## *🍉 view*

* LoginView가 해줌..

## *🍏 templates*

* 뻔한 내용이라 생략 

***

##  **🫵 로그 아웃**

## *🍊 url*

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
* 로그인과 동일하게 LogoutView 가 해줌.

## 로그인과 유사해서 생략.

##  **🫵 첫 페이지**

## *🍏 templates*

    {% if user.is_authenticated %}
        {% csrf_token %}
        <a href="{% url 'MBTIAPP:logout' %}">로그아웃</a>
        <a href="{% url 'MBTIAPP:mbtitest' %}">MBTI테스트 하기</a>
        <a href="{% url 'MBTIAPP:blog' %}">MBTI 게시판으로</a>
        {% endif %}

        {% if not user.is_authenticated %}
        {% csrf_token %}
        <a href="{% url 'MBTIAPP:login' %}">로그인</a>
        <a href="{% url 'MBTIAPP:signup' %}">회원가입</a>
    {% endif %}
* User가 로그인이 되어있지 않은데, MBTI검사를 시킬 순 없으므로 "user.is_authenticated" 를 사용하여,

* 로그인이 안된 상태라면, "로그인과 회원가입" 을.

* 로그인이 된 상태라면, "로그아웃/ MBTI테스트url / MBTI게시판url" 을 보여주게 설정 하였다.

***

# 2. MBTITEST / TEST 결과 / MBTI를 Profile에 저장

##  **🫵 MBTITEST + TEST결과**

## *🍊 url*
* 뻔함


## *🍋 form*

    class MbtiForm(forms.Form):
        EI = forms.ChoiceField(choices=[('E','네'),('I','아니오')], widget=forms.RadioSelect)
        NS = forms.ChoiceField(choices=[('N','네'),('S','아니오')], widget=forms.RadioSelect)
        TF = forms.ChoiceField(choices=[('F','네'),('T','아니오')], widget=forms.RadioSelect)
        PJ = forms.ChoiceField(choices=[('J','네'),('P','아니오')], widget=forms.RadioSelect)
* 어려웠음. MBTI 테스트를 하는 템플릿에서 Form형식으로 직접 코드를 짜려했지만, 그 결과를 조합해서 하나의 MBTI를 만들자니, 모든 경우를 if 문으로 처리하는 노가다를 해야할 것 같아서 하기 싫었음.

* [링크][https://www.geeksforgeeks.org/choicefield-django-forms/]       
* Form의 사용법을 잘 몰랐기에 배울 겸 알아보았는데 위의 링크에서 ChoiceField를 form에서 지정해줄 수 있다고 알려줌.


## *🍉 view*

    def result(request):
        if request.method == 'POST':
            form = MbtiForm(request.POST)
            if form.is_valid():
                EI = form.cleaned_data['EI']
                NS = form.cleaned_data['NS']
                TF = form.cleaned_data['TF']
                PJ = form.cleaned_data['PJ']
                arr=[EI, NS, TF, PJ]
                my_mbti = ''.join(arr)
                user = request.user
                user.user_mbti = my_mbti
                user.save()
                context = {'mymbti':my_mbti}
                return render(request, 'MBTIAPP/result.html', context)
    else:
        form = MbtiForm()
        context = {'form': form}
        return render(request, 'MBTIAPP/result.html',context)
* 일단 POST 방식일때, if문 진입. 폼 검사 후, EI 등등의 변수( 이름 마음대로 만들어도 됨 ) 에 아까 회원가입할 때 배운 form.cleaned_data로 form에 입력된 값들을 집어 넣는다.

* 그 다음 arr이란 리스트에 mbti들을 넣음, 그 후, join을 하여 my_mbti라는 변수를 만들어 거기에 리스트 요소들을 합쳐서 하나의 문자열로 만듬

* 그 후 저장. 결과 창으로 정보(my_mbti) 담아서 이동

* 뭔가 점프 투 장고같은 곳에 나오는 뻔한 내용이 아닌 내용을 내손으로 구현해보니 가장 재미있었던 부분.

## *🍏 templates*

    <h1>결과창임</h1>
    {{ mymbti }}
    <a href="{% url 'MBTIAPP:blog' %}">mbti 게시판으로 이동하기</a>

* 그냥 아까 만든 mymbti를 보여줌..

***

##  **🫵 MBTI를 Profile에 저장**

## *🍉 view*

    def result(request):
        if request.method == 'POST':
            form = MbtiForm(request.POST)
            if form.is_valid():
                EI = form.cleaned_data['EI']
                NS = form.cleaned_data['NS']
                TF = form.cleaned_data['TF']
                PJ = form.cleaned_data['PJ']
                arr=[EI, NS, TF, PJ]
                my_mbti = ''.join(arr)
                user = request.user
                user.user_mbti = my_mbti
                user.save()
                context = {'mymbti':my_mbti}
                return render(request, 'MBTIAPP/result.html', context)
        else:
            form = MbtiForm()
            context = {'form': form}
            return render(request, 'MBTIAPP/result.html',context)
* 보면 알겠지만, 아까 MBTI테스트의 view 코드이다.

* 어떠한 기능을 구현하는데에 있어 중요한 내용 같아서 따로 씀.

*
        user = request.user
        user.user_mbti = my_mbti
        user.save()

* ❗️ "user" 를 "request.user" 로 지정하여, 현재 이 동작을 수행한 "request.user" 정의 하기.

* ❗️ 아까 Abstractuser로 만든 Profile이라는 모델에 user_mbti라는 필드를 추가했었다. 여기서 user.user_mbti라고 표기할 수 있는 이유는 Abstractuser는 AUTH로 만든 User를 상속하기 때문.

* ❗️ 그 후 , 아직 빈칸인 user.user_mbti 에 my_mbti를 집어 넣어줌. (재검사 일시, 새로운 값으로 대체) => 저장함.

***

# 3. 게시글 CRUD

## *🍎 model*

    class Post(models.Model):
        title =models.CharField(max_length=50)
        poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,default=1)
        content = models.TextField()
    
        def __str__(self):
            return self.title
* 중요한 부분 : Poster라는 필드는 아까 만든 Profile모델을 참조해야함. 그런데, 그냥 Profile을 참조한다고 하면, 어느 부분이 계속 작동을 안해서 , 

* ❓settings.AUTH_USER_MODEL (AbstractUser를 사용할 때 setting.py에 지정해줌.) 을 가리키면 잘 작동함 (아직까지 이유 모름)

## *🍉 view*

## create

    def new(request):
        return render(request, 'MBTIAPP/postcreate.html')

    def postcreate(request):
        if(request.method == 'POST'):
            post = Post()
            post.title=request.POST['title']
            post.content=request.POST['content']
            post.poster = request.user
            post.save()     
        return redirect('MBTIAPP:blog')

* 사실 보편적인 기능이라, 구글에 잘 나와있음.

* postcreate 에서 "post" 를 Post(모델)을 가리키게 하고,

* Post의 필드들에 POST방식으로 받은 정보들을 저장해준 후,

* ❗️ Post모델의 poster는 아직 비어있으므로, "request.user" 을 불러와, 지금 이 동작을 수행한 user를 poster에 넣어준다

* 저장하기!

## read

    def blog(request):
        posts = Post.objects.all()
        context = {'posts':posts}
        return render(request, 'MBTIAPP/blog.html', context)
    
    def detail(request, pk):
        post_detail = get_object_or_404(Post, pk=pk)
        comments = post_detail.comment_set.all()
        context = {
            'post' : post_detail,
            'comments' : comments
        }
        return render(request, 'MBTIAPP/detail.html', context)
* 게시글 목록을 보는 기능과, 상세페이지 구현.

* 먼저, blog 함수 : "posts" 변수에 Post모델 담음. => blog.html로 정보 보냄, 끝.

* 다음, detail 함수 : "post_detail" 변수 만들고 Post모델 가져옴

* 여기엔 곧 설명할 댓글도 들어가므로, "comments" 라는 변수에 Comment 모델도 가져온다.

* render로 context에 담은 정보들 보냄.

## update

    def edit(request, pk):
        post = Post.objects.get(pk=pk)
        if request.method == 'POST':
            post.title=request.POST['title']
            post.content=request.POST['content']
            post.save()  
            return redirect('MBTIAPP:detail', pk)
        else:
            context = {
                'post' : post
            }
            return render(request, 'MBTIAPP/edit.html', context)
* "post" 라는 변수에 Post모델 가져옴.

* POST 방식일 떄 (수정하기 버튼을 눌러 제출할 떄)는, post의 객체들을 그냥 바꿔주고 저장!!

* GET 방식일 때 (수정하려고 들어왔을 때)는, 원래 쓰여있던 제목/글 들 (post) 를 보여줌.

## delete

    def delete(request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('MBTIAPP:blog')
* 간단하다. post의 pk 를 받아와서, post 지정해주고 그냥 지워주면 됨..

## *🍏 templates*

## Create
    <form action="{% url 'MBTIAPP:postcreate' %}" method="POST">
    {% csrf_token %}
        <label for="title">제목</label><br>
        <input type="text" name="title", id="title"><br>
        <label for="content">글 내용</label><br>
        <textarea name="content" id="content" cols="40" rows="20"></textarea><br>
        <input type="submit" value="작성하기">
    </form>
* form 태그를 이용해 정보 입력 후 제출

* ❗️ input의 name이 중요함. 이 name으로 view에서 POST방식으로 전달됨. ❗️

## Read
    {% for post in posts %}
    <div class="posts">
        <h2>글 제목</h2>
        <a href="{% url 'MBTIAPP:detail' post.pk %}">{{post.title}}</a>
        <h2>작성자</h2>
        <p>{{post.poster.nickname}}<span>({{ post.poster.user_mbti }})</span></p>
    </div>   
    {% endfor %}

* 게시글 리스트 페이지, for문을 돌려 post라는 변수를 이용해 posts안에 담긴 게시글의 수만큼 반복 됨.



        <h1>디테일페이지</h1>
        <div class="details">
            <a href="{% url 'MBTIAPP:blog' %}">게시판으로 돌아가기</a><br>
            <h2>제목</h2>
            <p>{{ post.title }}</p>
            <h2>내용</h2>
            <p>{{ post.content }}</p>
            <h2>작성자</h2>
            <span>{{ post.poster }}({{ post.poster.user_mbti }})</span><br><br><br>
            <a href="{% url 'MBTIAPP:edit' post.pk %}">수정하기</a>
            <a href="{% url 'MBTIAPP:delete' post.pk %}">삭제하기</a>
        </div>
* Detail 페이지 인데, 게시글 제목, 내용 보여주고 작성자 닉네임, mbti를 보여줌.

## Update는 유사하고 간단해서 생략.
## Delete는 템플릿 필요없음.

***

# 4. 댓글 CRED

## *🍎 model*

    class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    content = models.CharField(max_length=150)

        def __str__(self):
            return self.content
* Post와 비슷하다.

* 다른점 : Comment에서는 어느 Post에 달린 댓글인지를 구분해야 하기 때문에, post라는 필드를 만들어 Post모델을 외래키로 참조한다.

## *🍋 form*

    class CommentForm(forms.ModelForm):

        class Meta:
            model = Comment
            exclude = ('post','commenter')
* 댓글을 작성할 때, 댓글 내용만 입력받으면 되니, Comment모델에서 post와 commenter는 exlude로 빼줌. 
* form태그로 html상에서 처리할 수 있을 것 같지만 Form.py를 이용하는 개념이 애매해서 공부할 겸 form으로 만듬.
## *🍊 url*

    path('<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:post_pk>/comment/<int:comment_pk>/edit/', views.comment_edit, name='comment_edit'),
* ❗️ 중요한듯 하다. 보면, comment_create의 url은 pk/comment 형식 . pk는 post의 pk이다.

* ❗️ 핵심은 , delete와 edit은 댓글을 건드리는 url들 인데, 어느 게시물의 댓글인지 구분해야 하므로, post의 pk 와 comment의 pk를 둘다 url에 집어 넣어야 한다.

## *🍉 view*
## create
    def comment_create(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm()
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.commenter = request.user
                comment.save()
                return redirect('MBTIAPP:detail', pk)
        else:
            form = CommentForm()
        return render(request, 'MBTIAPP/detail.html', {'post':post, 'form': form})
* 헷갈려서 시간이 꽤나 걸림.. pk를 주고 받는 동작에 대한 공부가 잘 되었음.

* 먼저 is_authenticated (로그인상태) 일때, "post"라는 변수에 Post모델 가져옴. 

* 처음 POST방식 으로 들어갔을 때, "comment_form"이라는 변수에, CommentForm을 가져옴. => 폼 검사 후, 

* comment의 필드들에 필요한 정보들을 담는다.

* comment.post에는 이 글이 어떤 post인지 알기 위해 post를 담아줌

* commenter 에는 이 댓글을 단 사람이 누구인지 DB에 넣어주기 위해 request.user를 저장함.

* GET방식 일땐 빈폼을 보여줌.

* ❓ 의문인점) 위에 있는 form = CommentForm() 을 쓰기전에는 오류가 떠서 알아보니, if문 (POST방식)으로 들어가기 전에 form을 정의해주어야 한다고 함. 

* ❓ 그건 else문안의 GET방식에서 form = CommentForm() 입력해 두었으니 GET으로 받고 입력하고 POST보내도 되는거 아닌가?...

## delete

    def comment_delete(request, post_pk, comment_pk):
        if request.user.is_authenticated:
            comment = get_object_or_404(Comment, pk=comment_pk)
            if request.user == comment.commenter:
                comment.delete()
        return redirect('MBTIAPP:detail', post_pk) 
* post의 pk 와 comment의 pk 를 동시에 생각하느라 공부가 되었다.

* 어느 게시물의 어느댓글을 지울건지 알아야 하기 때문에, post와 comment의 pk를 둘다 인자로 받음.

* "comment"라는 변수에 Comment모델 받아옴, 당연히 이때 pk는 해당 댓글의 pk

* if 문으로 들어가서, 지금 이 동작을 수행하는 user와 comment를 작성한 user가 같다면, 지우게 실행. (근데 이건 어차피 html상에서 본인이 쓴 댓글이 아니면 삭제버튼 자체가 안뜨게 구현해놔서 큰 의미는 없지만 그냥 작성했음)

* 그리고 동작이 끝나면, detail페이지로 이동.

* ❗️ detail페이지로 이동할 땐 post의 디테일 페이지 이므로, post_pk를 보내준다 ! comment_pk는 필요없음!

## update는 유사해서 생략

## *🍏 templates*
    <h3>댓글들</h3>
    {% if comments %}
    <p>{{ comments|length }}개의 댓글이 있어요</p>
    {% endif %}
    <ul>
        {% for comment in comments %}
        <li>
            {{ comment.content }} - {{ comment.commenter }}<span>({{ comment.commenter.user_mbti }})</span>
            {% if user == comment.commenter %}
                <form action="{% url 'MBTIAPP:comment_delete' post.pk comment.pk %}">
                {% csrf_token %}
                <br><div class="buttons"><input type="submit" value="댓글삭제">
                </div>
                </form>
                <a href="{% url 'MBTIAPP:comment_edit' post.pk comment.pk %}">수정하기</a>
            {% endif %}
        </li>
        {% empty %}
            <p>No 댓글~</p>
        {% endfor %}
    </ul>
* 아까 comment라는 변수에 정보들을 담았으므로, if문을 이용해, comments에 접근.

* length를 이용해 comments 안에 담긴 댓글 개수를 추출.

* for문을 돌려, comments에 담긴 댓글 수 만큼 반복.

* 댓글 내용 , 닉네임 , mbti 표기.

* if문으로 들어가서, user가 댓글 작성자와 같을 경우, 댓글삭제와 수정하기 버튼이 보이게 함.

* 구글링하다보니, empty 라는 것도 있길래 써봄.

* ❗️ delete와 edit은 아까 말했듯이, post와 comment의 pk 둘다 필요로 하므로, 둘다 인자로 보내줘야함.

***

# ❗️회고

## *그럴듯한 기능들을 직접 만들어보니, 내가 장고를 얼마나 얕게 알고 있었는지 깨닫게 되었고, 이 과제 하나로 엄청난 양의 공부를 하게 되었고, readme 적으면서 또 한번 정리하니 좋았다.*

## *엉터리인 블로그들이 많다는 걸 다시 느낀다..*

## *중요한 점들이나 의문점들은 위에 다 적어놨음.*
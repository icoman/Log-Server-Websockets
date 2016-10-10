% include('header.tpl')

<script src="/static/jquery.min.js"></script>

  <script type="text/javascript">
  function newWindow(chan){
	//window.open('/log/'+chan,'log_'+chan,'width=1024,height=480,resizable=yes');
	window.open('/log/'+chan,'','width=1024,height=480,resizable=yes');
  }
  </script>

<h1>{{title}}</h1>
<a href="/">Home</a> <br>
%if channels:
Connect:
%for i in channels:
&nbsp;&nbsp;&nbsp;&nbsp;
<a href="#" onclick="JavaScript:newWindow('{{i}}')">{{i}}</a>	
%end
%else:
No log channels.
%end


	



% include('footer.tpl')

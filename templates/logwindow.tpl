% include('header.tpl')

<script src="/static/jquery.min.js"></script>

  <script type="text/javascript">
  var ws = null;
  function connect_channel(chan) {
	  if (!window.WebSocket) {
		if (window.MozWebSocket) {
			window.WebSocket = window.MozWebSocket;
		} else {
			$('#messages').append("<li>Your browser doesn't support WebSockets.</li>");
		}
	}

	if (ws) ws.close(); //inchide canal daca e deschis
    ws = new WebSocket("ws://localhost:8080/websocket/"+chan);
	ws.onopen = function(evt) {
                $('#messages').text('Connected to channel '+chan+'.');
            }
    ws.onmessage = function(evt) {
                //$('#messages').append('<li>' + evt.data + '</li>');
				$('#messages').append(evt.data);
            }
  }
  connect_channel('{{chan}}');
  </script>

<h1>{{title}}</h1>





<hr>
<form>
		<input type="button" value="Close" onclick="window.close()" />
		<input type="button" value="Clear" onclick="$('#messages').text('Log cleared.')" />
 </form>
 <div id="messages"></div>

	
	



% include('footer.tpl')

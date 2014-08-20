% include('header.tpl')
        <li><a href="/">Home</a></li>
        <li><a href="/accounts">Accounts</a></li>
        <li class="active"><a href="/blocks">Blocks</a></li>
        <li><a href="/payouts">Payouts</a></li>
		<li><a href="/unpaid">Unpaid</a></li>
		<li><a href="/paid">Paid</a></li>
        </ul>
      </div><!--/.nav-collapse -->
    </div>
  </div>
  
<div class="container">
  
  <div class="text-center">
  	<div class="page-header">
	<h1>Block List:</h1>
  	</div>
	<div class="col-lg-12">
	<h3>Estimated Time</h3>    
    <p><div id="btime"></div></p>
	</div>
	<script>
  $.getJSON('/api/btime', function(data) {
        var output="<p><strong>Until Next Block: </strong>" + data.blocktime + "</p>";
        document.getElementById("btime").innerHTML=output;
  });
    </script>
<div class="table-responsive">
<table class="table table-striped table-bordered table-condensed table-hover">
<tr><td><strong>Height</strong></td><td><strong>Timestamp</strong></td><td><strong>Block</strong></td><td><strong>Total Fee</strong></td></tr>
%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  </tr>
%end
</table>
</div>
</div>  
</div>
</div>
% include('footer.tpl')
% include('header.tpl')
        <li><a href="/">Home</a></li>
	<li><a href="/getting_started">Getting Started</a></li>
        <li><a href="/accounts">Accounts</a></li>
        <li class="active"><a href="/blocks">Blocks</a></li>
        <li class="dropdown">
          <a href="/payouts" class="dropdown-toggle" data-toggle="dropdown">
            Payout Data<b class="caret"></b>
          </a>
          <ul class="dropdown-menu">
            <li><a href="/payouts">Payouts</a></li>
			<li><a href="/unpaid">Unpaid</a></li>
			<li><a href="/paid">Paid</a></li>        
          </ul>
        </li>
        </ul>
        <div class="col-sm-3 col-md-3 pull-right">
            <form class="navbar-form" action="/user" role="form" method="post">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Account Name" name="username">
                    <div class="input-group-btn">
                        <button class="btn btn-default" type="submit"><i class="glyphicon glyphicon-search"></i></button>
                    </div>
                </div>
            </form>
         </div>
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
<table id="paid" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Height</th>
                <th>Total Fee</th>
            </tr>
        </thead>
    </table>
<script>
$(document).ready(function() {
    $('#paid').dataTable( {
        "ajax": {
            "url": "/api/blocks",
            "dataSrc": ""
        },
        "columns": [
            { "data": "timestamp" },
            { "data": "height" },
            { "data": "totalfee" }
        ],
        "order": [[ 0, "desc" ]],
        "lengthMenu": [[10, 20, 50, -1], [10, 20, 50, "All"]]
    } );
} );
</script>
</div>
</div>  
</div>
</div>
% include('footer.tpl')

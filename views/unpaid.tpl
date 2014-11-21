% include('header.tpl')
        <li><a href="/">Home</a></li>
        <li><a href="/getting_started">Getting Started</a></li>
        <li><a href="/accounts">Accounts</a></li>
        <li><a href="/blocks">Blocks</a></li>
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
		<h1>Unpaid Transactions:</h1>
		<h4>Total Unpaid: <small>{{unpaid}} NHZ</small></h4>
	</div>
</div>
<div class="table-responsive">
<table id="unpaid" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
                <th>Blocktime</th>
                <th>Account</th>
                <th>Percentage</th>
                <th>Amount</th>
            </tr>
        </thead>
    </table>
<script>
$(document).ready(function() {
    $('#unpaid').dataTable( {
        "ajax": {
            "url": "/api/unpaid",
            "dataSrc": ""
        },
        "columns": [
            { "data": "blocktime" },
            { "data": "account" },
            { "data": "percentage" },
            { "data": "amount" }
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

% include('header.tpl')
        <li><a href="/">Home</a></li>
        <li><a href="/getting_started">Getting Started</a></li>
        <li class="active"><a href="/accounts">Accounts</a></li>
        <li><a href="/blocks">Blocks</a></li>
        <li><a href="/payouts">Payouts</a></li>
		<li><a href="/unpaid">Unpaid</a></li>
		<li><a href="/paid">Paid</a></li>
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
<h1>Active Accounts List:</h1>
</div>
<div class="table-responsive">
<table id="accounts" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
                <th>Account</th>
                <th>Height From</th>
                <th>Height To</th>
                <th>Amount</th>
            </tr>
        </thead>
    </table>
<script>
$(document).ready(function() {
    $('#accounts').dataTable( {
        "ajax": {
            "url": "/api/accounts",
            "dataSrc": ""
        },
        "columns": [
            { "data": "ars" },
            { "data": "heightfrom" },
            { "data": "heightto" },
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
</div>
% include('footer.tpl')

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
		<h1>Payouts List:</h1>
	</div>
</div>
<div class="table-responsive">
<table id="paid" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
                <th>Account</th>
                <th>Payment</th>
                <th>Fee</th>
            </tr>
        </thead>
    </table>
<script>
$(document).ready(function() {
    $('#paid').dataTable( {
        "ajax": {
            "url": "/api/payouts",
            "dataSrc": ""
        },
        "columns": [
            { "data": "account" },
            { "data": "payment" },
            { "data": "fee" }
        ],
        "order": [[ 0, "desc" ]],
        "lengthMenu": [[10, 20, 50, -1], [10, 20, 50, "All"]]
    } );
} );
</script>
<div id="loctable"></div>
<script>
$.getJSON("/api/payouts", function(data) {
    $("#loctable").mrjsontable({
        tableClass: "my-table table-striped table-bordered table-condensed table-hover",
        pageSize: 10, //you can change the page size here
        columns: [
            new $.fn.mrjsontablecolumn({
                heading: "Account",
                data: "account"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Paid",
                data: "payment"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Fee",
                data: "fee"
            })
        ],
        data: data
    });
});
</script>
</div>
</div>  
</div>
</div>
% include('footer.tpl')

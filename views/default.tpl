% include('header.tpl')
        <li class="active"><a href="/">Home</a></li>
        <li><a href="/getting_started">Getting Started</a></li>
        <li><a href="/accounts">Accounts</a></li>
        <li><a href="/blocks">Blocks</a></li>
        <li><a href="/payouts">Payouts</a></li>
		<li><a href="/unpaid">Unpaid</a></li>
		<li><a href="/paid">Paid</a></li>
        </ul>
      </div><!--/.nav-collapse -->
    </div>
  </div>
  
  <!-- Begin page content -->
  <div class="container">
  <div class="text-center">
    <div class="page-header">
      <h1>NHZ Forging Pool</h1>
    </div>
<div class="row">
  <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
  <h3>Pool Account: <small>{{pa}}</small></h3>
   	<h4>Leased Amount: <small>{{nhzb}} NHZ</small></h4>
    <h4>Pool Fee is: <small>{{fee}}%</small></h4>
   
    <br>
    <em>Pool Interface is still in testing only raw data is displayed</em>
  </div> 
</div>
<div class="row">
  <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
  <h3>Active Accounts<p><small>at Last Block Found</p></small></h3>
  <div class="table-responsive">
<table class="table table-striped table-bordered table-condensed table-hover">
<tr><td><strong>Account</strong></td><td><strong>Last Block</strong></td><td><strong>Amount</strong></td></tr>
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
  <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
  <h3>Last Blocks<p><small>Found</p></small></h3>
    <div class="table-responsive">
<table class="table table-striped table-bordered table-condensed table-hover">
<tr><td><strong>Height</strong></td><td><strong>Timestamp</strong></td><td><strong>Amount</strong></td></tr>
%for row in blocks:
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
</div>
</div>
</div>
% include('footer.tpl')

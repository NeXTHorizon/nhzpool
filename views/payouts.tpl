% include('header.tpl')
        <li><a href="/">Home</a></li>
        <li><a href="/accounts">Accounts</a></li>
        <li><a href="/blocks">Blocks</a></li>
        <li class="active"><a href="/payouts">Payouts</a></li>
		<li><a href="/unpaid">Unpaid</a></li>
		<li><a href="/paid">Paid</a></li>
        </ul>
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
<table class="table table-striped table-bordered table-condensed table-hover">
<tr><td><strong>Account</strong></td><td><strong>Fee</strong></td><td><strong>Payment</strong></td></tr>
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
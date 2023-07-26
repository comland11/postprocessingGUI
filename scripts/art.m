% Generate 1D arrays along x, y, and z directions
x = linspace(-fov(1) / 2, fov(1) / 2, nPoints(1));
y = linspace(-fov(2) / 2, fov(2) / 2, nPoints(2));
z = linspace(-fov(3) / 2, fov(3) / 2, nPoints(3));

% Create 3D mesh grid from the 1D arrays
[y, z, x] = meshgrid(y, z, x);

% Reshape the mesh grid to 1D arrays
x = x(:);
y = y(:);
z = z(:);

% Perform iterative calculations for niter iterations
for n = 1:niter
    % Iterate through the sampled data 's'
    for t = 1:length(s)
        % Calculate mt using complex exponentials based on sampled data and 3D positions
        mt = exp(2 * pi * (-1i * sampled(t, 1) * x + 1i * sampled(t, 2) * y - 1i * sampled(t, 3) * z));

        % Calculate normalization factors for mt
        norm = dot(mt, mt);
        norm1 = mt' * mt;

        % Calculate delta_t, the update step for 'rho'
        delta_t = (-s(t) + mt' .* rho) / norm;

        % Update 'rho' using the calculated delta_t
        rho = rho - lbda .* delta_t .* mt';

        % Display progress
        fprintf('Iteration %i of %i\n', t, length(s));
    end
end

% Reshape 'rho' to match the original 3D shape
rho = reshape(rho, nPoints(end:-1:1));

% Save 'rho' in a .mat file
save('rho.mat', 'rho');
